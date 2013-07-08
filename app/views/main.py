import webapp2
import jinja2
import os
from app.models.models import Course, Registration, WinterSchoolFeedback, Subscription
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import mail
import datetime

import httplib
import urllib

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')))

class main(webapp2.RequestHandler):
    def get(self):
        q = db.GqlQuery("SELECT * FROM Course LIMIT 10")
        template_values = {
            'courses': q,
        }

        template = jinja_environment.get_template('main.html')
        self.response.out.write(template.render(template_values))


class about(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('about.html')
        self.response.out.write(template.render())


class courses(webapp2.RequestHandler):
    def get(self):
        course = self.request.get('course')
        if course != '':
            q = db.GqlQuery("SELECT * FROM Course LIMIT 10 WHERE title = :1", course)
        else:
            q = db.GqlQuery("SELECT * FROM Course LIMIT 10")

        courses = []
        for c in q:
            c.passed = c.rego_date < datetime.datetime.now()
            courses.append(c)

        template_values = {
            'courses': courses,
            'size': q.count(),
        }
        template = jinja_environment.get_template('courses.html')
        self.response.out.write(template.render(template_values))

class course(webapp2.RequestHandler):
    def get(self, id):
        c = Course.get_by_id(int(id))
        c.passed = c.rego_date < datetime.datetime.now()

        template_values = {
            'courses': [c],
            'size': 1,
        }
        template = jinja_environment.get_template('courses.html')
        self.response.out.write(template.render(template_values))

class signup(webapp2.RequestHandler):
     def get(self):
        course = Course.get_by_id(int(self.request.get('id')))
        template_values = {
            'year': self.request.get('year'),
            'level': self.request.get('level'),
            'course': course
        }
        template = jinja_environment.get_template('signup.html')
        self.response.out.write(template.render(template_values))

     def post(self):
        course = Course.get_by_id(int(self.request.get('course')))
        r = Registration(parent=course)
        r.email = self.request.get('email')
        r.emergency_contact_name = self.request.get('emergency_contact_name')
        r.emergency_contact_number = self.request.get('emergency_contact_number')
        r.full_name = self.request.get('full_name')
        r.highschool = self.request.get('highschool')
        r.laptop = bool(self.request.get('laptop'))
        r.level = int(self.request.get('level'))
        r.year = int(self.request.get('year'))
        r.gender = self.request.get('gender')
        r.put()

        # Send an email to them
        message = mail.EmailMessage(sender="UNSW Comp Club <admin@compclub.com.au>",
                            subject="Thank you for signing up to " + course.title + "!")

        message.to = r.full_name + " <" + r.email + ">"
        message.bcc = "champs@compclub.com.au"
        message.body = """
Dear """ + r.full_name + """,

Welcome to UNSW Computing Club! You've successfully signed up to """ + course.title + """. An email with
additional information will be sent to you shortly before the module begins.

Should you have any questions, feel free to contact us at team@compclub.com.au.

UNSW Computing Club
        """

        message.send()

        template_values = {
            'email': r.email,
        }
        template = jinja_environment.get_template('thanks.html')
        self.response.out.write(template.render(template_values))

class subscription(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('subscription.html')
        self.response.out.write(template.render())
    def post(self):
        subscribe = Subscription()
        subscribe.name = self.request.get('name')
        subscribe.email = self.request.get('email')
        subscribe.sub_type = self.request.get('sub_type')
        subscribe.put()

        template = jinja_environment.get_template('thanks_subscription.html')
        self.response.out.write(template.render())



class wizard(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('wizard.html')
        self.response.out.write(template.render())
    def post(self):
        q = db.GqlQuery("SELECT * FROM Course LIMIT 10")
        year = int(self.request.get('year'))
        experience = int(self.request.get('experience'))
        courses = []
        for c in q:
            if c.from_year <= year and year <= c.to_year and c.minlevel <= experience and experience <= c.maxlevel:
                c.passed = c.rego_date < datetime.datetime.now()
                courses.append(c)

        template_values = {
            'courses': courses,
            'size': len(courses),
            'year': year,
            'level': experience
        }

        template = jinja_environment.get_template('courses.html')
        self.response.out.write(template.render(template_values))

class feedback(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('feedback.html')
        self.response.out.write(template.render())

    def post(self):
        feedback = WinterSchoolFeedback()
        feedback.course = self.request.get('course')
        feedback.aims_module_clear = int(self.request.get('aims_module_clear'))
        feedback.challenging_interesting = int(self.request.get('challenging_interesting'))
        feedback.presenter_effective = int(self.request.get('presenter_effective'))
        feedback.would_recommend = int(self.request.get('would_recommend'))
        feedback.overall_satisfied = int(self.request.get('overall_satisfied'))
        feedback.best_part = self.request.get('best_part')
        feedback.worst_part = self.request.get('worst_part')
        feedback.other_comments = self.request.get('other_comments')
        feedback.put()

        template = jinja_environment.get_template('thanks_feedback.html')
        self.response.out.write(template.render())
