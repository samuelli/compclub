import webapp2
import jinja2
import os
from app.models.models import Course, Registration
from google.appengine.ext import db
from google.appengine.api import users
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
