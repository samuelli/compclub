import webapp2
import jinja2
import os
import re
from app.models.models import Course, Registration, Subscription, Roll
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import mail
from datetime import datetime
import httplib
import urllib
import logging

#function to replace tag with string
def replaceTagWithString(tagName, newString, sourceString):
    tag = "<<"+tagName+">>"
    replacedString = re.sub(tag, newString, sourceString)
    return replacedString

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

        # allow_button determines whether a 'Register' button should be displayed
        # for that particular course
        # TODO: allow a custom URL for the button to be specified?
        if self.request.get('allow_button'):
            c.allow_button = True
        else:
            c.allow_button = False

        c.put()

        q = db.GqlQuery("SELECT * FROM Course LIMIT 10")
        template_values = {
            'courses': q,
            'size': q.count(),
            'users': users,
        }

        template = jinja_environment.get_template('courses.html')
        self.response.out.write(template.render(template_values))

class rollmark(webapp2.RequestHandler):
    def get(self, course):
        c = Course.get_by_id(int(course))

        q = db.GqlQuery("SELECT * FROM Registration WHERE ANCESTOR IS :1", c)
        q = sorted(q, key=lambda x: x.full_name)

        template_values = {
            'course': c,
            'regos': q,
            'users': users,
        }

        template = jinja_environment.get_template('roll.html')
        self.response.out.write(template.render(template_values))
    def post(self, course):
        c = Course.get_by_id(int(course))
        date = datetime.strptime(self.request.get('roll_date'), '%Y-%m-%d')
        present = self.request.get_all("present")
        r = Roll();
        r.students = present
        r.course_name = c.title
        r.date = date
        r.put();

        regos = db.GqlQuery("SELECT * FROM Registration WHERE ANCESTOR IS :1", c)
        registrations = [r.full_name for r in regos]

        template_values = {
            'course': c.title,
            'date': date.date(),
            'regos': registrations,
            'students': present
        }

        template = jinja_environment.get_template('rollview.html')
        self.response.out.write(template.render(template_values))

class rollview(webapp2.RequestHandler):
    def get(self, course):
        c = Course.get_by_id(int(course))

        rolls = db.GqlQuery("SELECT * FROM Roll WHERE course_name =:1", c.title)
        rolls = sorted(rolls, key=lambda x: x.date)

        template_values = {
            'course': c,
            'rolls': rolls
        }

        template = jinja_environment.get_template('rolldateselect.html')
        self.response.out.write(template.render(template_values))
    def post(self, course):
        c = Course.get_by_id(int(course))
        date = datetime.strptime(self.request.get('date'), '%Y-%m-%d')

        regos = db.GqlQuery("SELECT * FROM Registration WHERE ANCESTOR IS :1", c)
        registrations = [r.full_name for r in regos]

        rolls = db.GqlQuery("SELECT * FROM Roll WHERE course_name =:1 AND date =:2", c.title, date)
        students = [s for r in rolls for s in r.students]

        template_values = {
            'course': c.title,
            'date': date.date(),
            'regos': registrations,
            'students': students
        }

        template = jinja_environment.get_template('rollview.html')
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
        sent = True if self.request.get('sent') == "true" else False

        s = db.GqlQuery("SELECT * FROM Subscription WHERE sub_type = 'student'")
        t = db.GqlQuery("SELECT * FROM Subscription WHERE sub_type = 'teacher'")
        p = db.GqlQuery("SELECT * FROM Subscription WHERE sub_type = 'parent'")

        template_values = {
            'student': s,
            'teacher': t,
            'parent': p,
            'sent': sent,
        }
        template = jinja_environment.get_template('emailing.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        emails = self.request.get_all('emails')
        email_subject = self.request.get('email_subject')
        email_bcc = self.request.get('email_bcc')
        original_email_body = self.request.get('email_body')

        # Send an email to each email
        for email in emails:
            #get person's name from database
            #re.sub() remove duplicate white spaces
            #.strip() remove whitespaces from the start and end of name
            n = db.GqlQuery("SELECT * FROM Subscription WHERE email =:1", email).get()
            name = re.sub('\s+', ' ', n.name).strip()
            #print "person's name: " + name

            #insert person's name to the tag <<NAME>>
            email_body = replaceTagWithString("NAME", name, original_email_body)
            #print email_body

            #person's ID (based on database unique ID
            person_id = str(n.key().id())
            #print person_id
            #print "%s" % emails
            unlink = "http://www.compclub.com.au/unsubscribe/" + person_id
            #make UNSUBSCRIBE link
            email_body = replaceTagWithString("UNSUBSCRIBE", unlink, email_body)
            print email_body

            message = mail.EmailMessage(sender="UNSW Comp Club <admin@compclub.com.au>", subject=email_subject)
            message.to = name + " <" + email + ">"
            message.bcc = email_bcc
            message.html = email_body

            message.send()
        self.redirect('/admin/emailing?sent=true')

class update(webapp2.RequestHandler):
    def post(self, course):
        c = Course.get_by_id(int(course))

        c.description = self.request.get('desc')
        c.allow_button = bool(self.request.get('allow_button'))
        c.put()

        q = db.GqlQuery("SELECT * FROM Course LIMIT 10")
        template_values = {
            'courses': q,
            'size': q.count(),
            'users': users,
        }

        template = jinja_environment.get_template('courses.html')
        self.response.out.write(template.render(template_values))