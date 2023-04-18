from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Student, Tutor
from werkzeug.security import generate_password_hash,  check_password_hash
from . import db
import json

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return "<p>Login</p>"


@auth.route('/tutorRegistration', methods=['GET', 'POST'])
def tutorRegistration():
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
                              password=generate_password_hash(
                                  password, method='sha256'),
                              phone_number=phoneNumber, subjects=subject, days=days,
                              monday_time=mondayTime, tuesday_time=tuesdayTime,
                              wednesday_time=wednesdayTime, thursday_time=thursdayTime,
                              friday_time=fridayTime, saturday_time=saturdayTime,
                              sunday_time=sundayTime, total_hours=0,
                              profile_pic=profilePic.read(), bio=aboutMe)
            db.session.add(new_tutor)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.registered'))
    return render_template('tutorRegistration.html')


@auth.route('/studentRegistration', methods=['GET', 'POST'])
def studentRegistration():
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
            flash('Password don\'t match.', category='error')
        elif len(password) < 7:
            flash('Email must be at least 7 characters', category='error')
        else:
            new_student = Student(first_name=firstName, last_name=lastName, email=email,
                                  password=generate_password_hash(
                                      password, method='sha256'),
                                  phone_number=phoneNumber, total_hours=0, fav_tutors='')
            db.session.add(new_student)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.registered'))
    return render_template('studentRegistration.html')


@auth.route('/crappt', methods=['GET', 'POST'])
def crappt():

    if request.method == 'POST':
        mondayTime = json.dumps(request.form.getlist('mondayTime'))
        tuesdayTime = json.dumps(request.form.getlist('tuesdayTime'))
        wednesdayTime = json.dumps(request.form.getlist('wednesdayTime'))
        thursdayTime = json.dumps(request.form.getlist('thursdayTime'))
        fridayTime = json.dumps(request.form.getlist('fridayTime'))
        saturdayTime = json.dumps(request.form.getlist('saturdayTime'))
        sundayTime = json.dumps(request.form.getlist('sundayTime'))

        print(mondayTime)

    our_tutors = Tutor.query.order_by(Tutor.id)

    return render_template("createApt.html", our_tutors=our_tutors)
