from . import db
from flask_login import UserMixin

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    phone_number = db.Column(db.String(20))
    # Not sure if needed
    appointments = db.relationship('Appointment')

class Tutor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    phone_number = db.Column(db.String(20))
    # Not sure if needed
    appointments = db.relationship('Appointment')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime())
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'))