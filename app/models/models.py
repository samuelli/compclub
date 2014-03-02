from google.appengine.ext import db


class Course(db.Model):
    title = db.StringProperty()
    from_year = db.IntegerProperty()
    to_year = db.IntegerProperty()
    rego_date = db.DateTimeProperty()
    description = db.TextProperty()
    minlevel = db.IntegerProperty()
    maxlevel = db.IntegerProperty()
    allow_button = db.BooleanProperty()
    # Created
    created = db.DateTimeProperty(auto_now_add=True)


# Parent = course
class Registration(db.Model):
    full_name = db.StringProperty()
    gender = db.CategoryProperty()
    email = db.EmailProperty()
    highschool = db.StringProperty()
    emergency_contact_name = db.StringProperty()
    emergency_contact_number = db.StringProperty()
    laptop = db.BooleanProperty()
    year = db.IntegerProperty()
    level = db.IntegerProperty()
    reason = db.StringProperty()

    # Created
    created = db.DateTimeProperty(auto_now_add=True)

class Roll(db.Model):
    course_name = db.StringProperty()
    date = db.DateTimeProperty()
    students = db.StringListProperty()
    # Created
    created = db.DateTimeProperty(auto_now_add=True)

class WorkshopFeedback(db.Model):
    # Course
    course = db.StringProperty()
    # Feedback
    aims_module_clear = db.IntegerProperty()
    challenging_interesting = db.IntegerProperty()
    presenter_effective = db.IntegerProperty()
    would_recommend = db.IntegerProperty()
    overall_satisfied = db.IntegerProperty()
    best_part = db.TextProperty()
    worst_part = db.TextProperty()
    other_comments = db.TextProperty()
    year = db.IntegerProperty()


class Subscription(db.Model):
    name = db.StringProperty()
    email = db.EmailProperty()
    sub_type = db.StringProperty()