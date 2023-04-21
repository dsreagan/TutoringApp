from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Student, Tutor
from werkzeug.security import generate_password_hash,  check_password_hash
from . import db
import json

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        student = Student.query.filter_by(email=email).first()
        tutor = Tutor.query.filter_by(email=email).first()
        if student:
            if check_password_hash(student.password, password):
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.student_home'))
            else:
                flash('Incorrect password, try again.', category='error')
        elif tutor:
            if check_password_hash(tutor.password, password):
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.tutor_home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html')

@auth.route('/student-registration', methods=['GET', 'POST'])
def student_registration():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        phoneNumber = request.form.get('phoneNumber')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password != confirmPassword:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Email must be at least 7 characters', category='error')
        else:
            new_student = Student(first_name=firstName, last_name=lastName, email=email,
                                   password=generate_password_hash(password, method='sha256'),
                                   phone_number=phoneNumber, total_hours=0, fav_tutors='')
            db.session.add(new_student)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.registered'))
    return render_template('student-registration.html')

@auth.route('/tutor-registration', methods=['GET', 'POST'])
def tutor_registration():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        phoneNumber = request.form.get('phoneNumber')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        subject = json.dumps(request.form.getlist('subject'))
        days = json.dumps(request.form.getlist('day'))
        mondayTime = json.dumps(request.form.getlist('mondayTime'))
        tuesdayTime = json.dumps(request.form.getlist('tuesdayTime'))
        wednesdayTime = json.dumps(request.form.getlist('wednesdayTime'))
        thursdayTime = json.dumps(request.form.getlist('thursdayTime'))
        fridayTime = json.dumps(request.form.getlist('fridayTime'))
        saturdayTime = json.dumps(request.form.getlist('saturdayTime'))
        sundayTime = json.dumps(request.form.getlist('sundayTime'))
        profilePic = request.files['file']
        aboutMe = request.form.get('about')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password != confirmPassword:
            flash('Password don\'t match.', category='error')
        elif len(password) < 7:
            flash('Email must be at least 7 characters', category='error')
        else:
            new_tutor = Tutor(first_name=firstName, last_name=lastName, email=email,
                                password=generate_password_hash(password, method='sha256'),
                                phone_number=phoneNumber, subjects=subject, days=days,
                                monday_time=mondayTime, tuesday_time=tuesdayTime,
                                wednesday_time=wednesdayTime, thursday_time=thursdayTime,
                                friday_time=fridayTime, saturday_time=saturdayTime,
                                sunday_time=sundayTime, total_hours=0, 
                                profile_pic=profilePic.read(), bio = aboutMe)
            db.session.add(new_tutor)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.registered'))
    return render_template('tutor-registration.html')