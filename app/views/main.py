import webapp2
import jinja2
import os
from app.models.models import Course, Registration
from google.appengine.ext import db
from google.appengine.api import users

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
        template_values = {
            'courses': q,
            'size': q.count(),
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

        template_values = {
            'email': r.email,
        }
        template = jinja_environment.get_template('thanks.html')
        self.response.out.write(template.render(template_values))

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
                courses.append(c)

        template_values = {
            'courses': courses,
            'size': len(courses),
            'year': year,
            'level': experience
        }

        template = jinja_environment.get_template('courses.html')
        self.response.out.write(template.render(template_values))
