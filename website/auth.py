from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Student, Tutor
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
import json
import re

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
                login_user(student, remember=True)
                return redirect(url_for('views.student_home'))
            else:
                flash('Incorrect password, try again.', category='error')
        elif tutor:
            if check_password_hash(tutor.password, password):
                flash('Logged in successfully!', category='success')
                login_user(tutor, remember=True)
                return redirect(url_for('views.tutor_home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index', user=current_user))

@auth.route('/student-registration', methods=['GET', 'POST'])
def student_registration():
    errors = {}
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        phoneNumber = request.form.get('phoneNumber')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        studentEmailExists = Student.query.filter_by(email=email).first()
        tutorEmailExists = Tutor.query.filter_by(email=email).first()

        if not (firstName or firstName.isalpha()):
            errors["firstName"] = ["First name required and alphabet only"]
        elif not (lastName or lastName.isalpha()):
            errors["lastName"] = ["Last name required and alphabet only"]
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', email):
            errors["email"] = ["Email incorrect format"]
        elif studentEmailExists or tutorEmailExists:
            errors["email"] = ["Email already exists"]
        elif not phoneNumber:
            errors["phoneNumber"] = ["Phone number required"]
        elif not re.match(r'^\d{10}$', phoneNumber):
            errors["phoneNumber"] = ["Phone number should be 10 digits no dashes"]
        elif not password:
            errors["password"] = ["Password cannot be empty"]
        elif not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()]).+$', password):
            errors["password"] = ["Password does not follow rules"]
        elif password != confirmPassword:
            errors["confirmPassword"] = ["Passwords do not match"]
        else:
            new_student = Student(first_name=firstName, last_name=lastName, email=email,
                                   password=generate_password_hash(password, method='sha256'),
                                   phone_number=phoneNumber, total_hours=0, fav_tutors='')
            db.session.add(new_student)
            db.session.commit()
            login_user(new_student, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.registered'))
    return render_template('student-registration.html', user=current_user, errors=errors)

@auth.route('/tutor-registration', methods=['GET', 'POST'])
def tutor_registration():
    errors = {}
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
        about = request.form.get('about')

        studentEmailExists = Student.query.filter_by(email=email).first()
        tutorEmailExists = Tutor.query.filter_by(email=email).first()

        if not (firstName or firstName.isalpha()):
            errors["firstName"] = ["First name required and alphabet only"]
        elif not (lastName or lastName.isalpha()):
            errors["lastName"] = ["Last name required and alphabet only"]
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$', email):
            errors["email"] = ["Email incorrect format"]
        elif studentEmailExists or tutorEmailExists:
            errors["email"] = ["Email already exists"]
        elif not phoneNumber:
            errors["phoneNumber"] = ["Phone number required"]
        elif not re.match(r'^\d{10}$', phoneNumber):
            errors["phoneNumber"] = ["Phone number should be 10 digits no dashes"]
        elif not password:
            errors["password"] = ["Password cannot be empty"]
        elif not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()]).+$', password):
            errors["password"] = ["Password does not follow rules"]
        elif password != confirmPassword:
            errors["confirmPassword"] = ["Passwords do not match"]
        elif not about:
            errors["about"] = ["About section required"]
        elif not re.match(r'^[a-zA-Z0-9.\s]*$', about):
            errors["about"] = ["Characters/numbers/spaces only"]

        else:
            new_tutor = Tutor(first_name=firstName, last_name=lastName, email=email,
                                password=generate_password_hash(password, method='sha256'),
                                phone_number=phoneNumber, subjects=subject, days=days,
                                monday_time=mondayTime, tuesday_time=tuesdayTime,
                                wednesday_time=wednesdayTime, thursday_time=thursdayTime,
                                friday_time=fridayTime, saturday_time=saturdayTime,
                                sunday_time=sundayTime, total_hours=0, 
                                profile_pic=profilePic.read(), bio = about)
            db.session.add(new_tutor)
            db.session.commit()
            login_user(new_tutor, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.registered'))
    return render_template('tutor-registration.html', user=current_user, errors=errors)
