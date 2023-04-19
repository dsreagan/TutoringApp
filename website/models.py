from . import db
from flask_login import UserMixin


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    total_hours = db.Column(db.Float)
    fav_tutors = db.Column(db.String(150))
    appointments = db.relationship('Appointment', backref='student')

class Tutor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    subjects = db.Column(db.String(100))
    days = db.Column(db.String(100))
    monday_time = db.Column(db.String(20))
    tuesday_time = db.Column(db.String(20))
    wednesday_time = db.Column(db.String(20))
    thursday_time = db.Column(db.String(20))
    friday_time = db.Column(db.String(20))
    saturday_time = db.Column(db.String(20))
    sunday_time = db.Column(db.String(20))
    total_hours = db.Column(db.Float)
    profile_pic = db.Column(db.LargeBinary)
    bio = db.Column(db.Text)
    appointments = db.relationship('Appointment', backref='tutor')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    time = db.column(db.Time)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'))
    appointment_info = db.Column(db.Text)
    zoom_link = db.Column(db.Text)