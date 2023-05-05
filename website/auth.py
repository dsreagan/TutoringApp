from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Student, Tutor, Appointment
from . import db
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
import json
import re
import mimetypes
import base64
import io
from datetime import datetime
import jwt
import requests
from time import time

auth = Blueprint('auth', __name__)

@auth.route('/zoom',methods = ['POST', "GET"])
def zoom():
    decoded_data = 0
    file_type = 0
    appts_Table = request.args.get('appt_Table')
    appt_found = Appointment.query.join(Tutor, Tutor.id == Appointment.tutor_id).filter(
        Appointment.student_id == current_user.get_id())
    # print(current_user.get_id())
    # print(appt_found)
    tutorNames_found = Tutor.query.join(Appointment, Tutor.id == Appointment.tutor_id).filter(
        Appointment.student_id == current_user.get_id()).all()
    # print(tutorNames_found)
    JoinedRows = []
    for appt in appt_found:
        for tutor in tutorNames_found:
            if tutor.id == appt.tutor_id:
                JoinedRows.append(
                    [appt, str(tutor.first_name + ' ' + tutor.last_name)])

    tutor_search = request.args.get('tutor_search')
    if tutor_search:
        tutor_all = Tutor.query.filter(Tutor.first_name.contains(
            tutor_search) | Tutor.last_name.contains(tutor_search) | Tutor.id.contains(tutor_search))
    else:
        tutor_all = Tutor.query.all()

    for tutor in tutor_all:
        user_id = tutor.id
        user_row = Tutor.query.filter_by(id=user_id).first()
        binary_data = user_row.profile_pic
        file_obj = io.BytesIO(binary_data)
        decoded_data = base64.b64encode(file_obj.read()).decode('utf-8')
        file_type, encoding = mimetypes.guess_type(user_row.profile_picname)

    tutor_search = request.args.get('tutor_search')
    if tutor_search:
        tutor_all = Tutor.query.filter(Tutor.first_name.contains(tutor_search) | Tutor.last_name.contains(tutor_search) | Tutor.id.contains(tutor_search))
    else:
        tutor_all = Tutor.query.all()
    API_KEY = 'qecUpEX1SUGYDoNDH22qng'
    API_SEC = 'FZxPYx6U2sBIwJUe3X7Nsr1mzMONgFipllnS'

    token = jwt.encode(
        {'iss': API_KEY, 'exp': time() + 5000},

        API_SEC,
        algorithm='HS256'
    )

    meetingdetails = {"topic": "Online Tutoring Appointment",
                  "type": 2,
                  "start_time": "2019-06-14T10: 21: 57",
                  "duration": "45",
                  "timezone": "Europe/Madrid",
                  "agenda": "test",
 
                  "recurrence": {"type": 1,
                                 "repeat_interval": 1
                                 },
                  "settings": {"host_video": "true",
                               "participant_video": "true",
                               "join_before_host": "False",
                               "mute_upon_entry": "False",
                               "watermark": "true",
                               "audio": "voip",
                               "auto_recording": "cloud"
                               }
                  }
    
    headers = {'authorization': 'Bearer ' + token,
               'content-type': 'application/json'}
    r = requests.post(
        f'https://api.zoom.us/v2/users/me/meetings',
        headers=headers, data=json.dumps(meetingdetails))
 
    y = json.loads(r.text)
    join_URL = y["join_url"]
    meetingPassword = y["password"]
    return render_template("student-home.html", user = current_user, join_URL = join_URL, tutor_all=tutor_all, data=decoded_data, fileType=file_type, appointments=JoinedRows)

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
            errors["phoneNumber"] = [
                "Phone number should be 10 digits no dashes"]
        elif not password:
            errors["password"] = ["Password cannot be empty"]
        elif not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()]).+$', password):
            errors["password"] = ["Password does not follow rules"]
        elif password != confirmPassword:
            errors["confirmPassword"] = ["Passwords do not match"]
        else:
            new_student = Student(first_name=firstName, last_name=lastName, email=email,
                                  password=generate_password_hash(
                                      password, method='sha256'),
                                  phone_number=phoneNumber, total_hours=0, fav_tutors='')
            db.session.add(new_student)
            db.session.commit()
            login_user(new_student, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.student_home'))
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
        profilePicName = profilePic.filename
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
            errors["phoneNumber"] = [
                "Phone number should be 10 digits no dashes"]
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
                                profile_pic=profilePic.read(), 
                                profile_picname=profilePicName,
                                bio = about)

            db.session.add(new_tutor)
            db.session.commit()
            login_user(new_tutor, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.tutor_home'))
    return render_template('tutor-registration.html', user=current_user, errors=errors)
