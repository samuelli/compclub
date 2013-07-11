import webapp2
import jinja2
import os
import re
from app.models.models import Course, Registration, Subscription
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import mail
from datetime import datetime
import httplib
import urllib

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')))

class main(webapp2.RequestHandler):
    def get(self):

        q = db.GqlQuery("SELECT * FROM Course LIMIT 10")
        template_values = {
            'courses': q,
            'size': q.count(),
            'users': users,
        }

        template = jinja_environment.get_template('courses.html')
        self.response.out.write(template.render(template_values))

class create(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('createCourse.html')
        self.response.out.write(template.render())
    def post(self):
        c = Course()
        c.title = self.request.get('title')
        c.from_year = int(self.request.get('from_year'))
        c.to_year = int(self.request.get('to_year'))
        c.description = self.request.get('description')
        c.rego_date = datetime.strptime(self.request.get('rego_date'), '%Y-%m-%d')
        c.minlevel = int(self.request.get('minlevel'))
        c.maxlevel = int(self.request.get('maxlevel'))
        c.put()

        q = db.GqlQuery("SELECT * FROM Course LIMIT 10")
        template_values = {
            'courses': q,
            'size': q.count(),
            'users': users,
        }

        template = jinja_environment.get_template('courses.html')
        self.response.out.write(template.render(template_values))

class rego(webapp2.RequestHandler):
    def get(self, course):
        c = Course.get_by_id(int(course))

        q = db.GqlQuery("SELECT * FROM Registration WHERE ANCESTOR IS :1", c)

        template_values = {
            'course': c,
            'regos': q,
            'users': users,
        }

        template = jinja_environment.get_template('regos.html')
        self.response.out.write(template.render(template_values))

class emailing(webapp2.RequestHandler):
    def get(self):

        s = db.GqlQuery("SELECT * FROM Subscription WHERE sub_type = 'student'")
        t = db.GqlQuery("SELECT * FROM Subscription WHERE sub_type = 'teacher'")
        p = db.GqlQuery("SELECT * FROM Subscription WHERE sub_type = 'parent'")

        template_values = {
            'student': s,
            'teacher': t,
            'parent': p,
        }
        template = jinja_environment.get_template('emailing.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        emails = self.request.get_all('emails')
        email_subject = self.request.get('email_subject')
        email_body = self.request.get('email_body')

        # Send an email to each email
        for email in emails:
            #get person's name from database
            n = db.GqlQuery("SELECT * FROM Subscription WHERE email =:1", email).get()
            #re.sub() remove duplicate white spaces
            #.strip() remove whitespaces from the start and end of name
            name = re.sub('\s+', ' ', n.name).strip()
            #print name
            #print "%s" % emails

            message = mail.EmailMessage(sender="UNSW Comp Club <admin@compclub.com.au>", subject=email_subject)
            message.to = name + " <" + email + ">"
            message.bcc = "champs@compclub.com.au"
            #insert person's name to the first line of email body
            message.body = "Dear "+ name + email_body
            #print "Dear "+ name + email_body
            #message.send()

class update(webapp2.RequestHandler):
    def post(self, course):
        c = Course.get_by_id(int(course))

        c.description = self.request.get('desc')
        c.put()

        q = db.GqlQuery("SELECT * FROM Course LIMIT 10")
        template_values = {
            'courses': q,
            'size': q.count(),
            'users': users,
        }

        template = jinja_environment.get_template('courses.html')
        self.response.out.write(template.render(template_values))