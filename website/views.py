from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import *
import mimetypes
import base64
import io
from . import db
import json
import datetime
from datetime import date, timedelta
import calendar


views = Blueprint('views', __name__)


@views.route('/')
def index():
    decoded_data = 0
    file_type = 0
    tutor_search = request.args.get('tutor_search')
    if tutor_search:
        tutor_all = Tutor.query.filter(Tutor.first_name.contains(tutor_search) | Tutor.last_name.contains(
            tutor_search) | Tutor.id.contains(tutor_search) | Tutor.subjects.contains(tutor_search)).all()
    else:
        tutor_all = Tutor.query.all()
    for tutor in tutor_all:
        user_id = tutor.id
        user_row = Tutor.query.filter_by(id=user_id).first()
        binary_data = user_row.profile_pic
        file_obj = io.BytesIO(binary_data)
        decoded_data = base64.b64encode(file_obj.read()).decode('utf-8')
        file_type, encoding = mimetypes.guess_type(user_row.profile_picname)

    return render_template('index.html', user=current_user, tutor_all=tutor_all, data=decoded_data, fileType=file_type)


@views.route('/student')
@login_required
def student_home():
    decoded_data = 0
    file_type = 0
    appts_Table = request.args.get('appt_Table')
    appt_found = Appointment.query.join(Tutor, Tutor.id == Appointment.tutor_id).filter(
        Appointment.student_id == current_user.get_id())
    # print(current_user.get_id())
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

    return render_template('student-home.html', user=current_user, tutor_all=tutor_all, data=decoded_data, fileType=file_type, appointments=JoinedRows)


@views.route('/tutor')
@login_required
def tutor_home():

    user_id = current_user.id
    user_row = Tutor.query.filter_by(id=user_id).first()
    binary_data = user_row.profile_pic
    file_obj = io.BytesIO(binary_data)
    decoded_data = base64.b64encode(file_obj.read()).decode('utf-8')
    file_type, encoding = mimetypes.guess_type(user_row.profile_picname)
    return render_template('tutor-home.html', user=current_user)

    appts_Table = request.args.get('fixedTable')
    appt_found = Appointment.query.join(Tutor, Tutor.id == Appointment.tutor_id).filter(
        Appointment.tutor_id == current_user.get_id())
    print(current_user.get_id())
    print(appt_found)
    studentNames_found = Student.query.join(Appointment, Student.id == Appointment.student_id).filter(
        Appointment.tutor_id == current_user.get_id()).all()
    print(studentNames_found)
    JoinedRows = []
    for appt in appt_found:
        for student in studentNames_found:
            if student.id == appt.student_id:
                JoinedRows.append(
                    [appt, str(student.first_name + ' ' + student.last_name)])

    return render_template('tutor-home.html', user=current_user, appointments=JoinedRows, data=decoded_data, fileType=file_type)


@views.route('/apptConfirmation')
def apptCreated():
    return render_template('appt-created.html', user=current_user)


@views.route('/crappt', methods=['GET', 'POST'])
def make_appointment():
    if request.method == 'POST':
        mondayTime = json.dumps(request.form.getlist('mondayTime'))
        tuesdayTime = json.dumps(request.form.getlist('tuesdayTime'))
        wednesdayTime = json.dumps(request.form.getlist('wednesdayTime'))
        thursdayTime = json.dumps(request.form.getlist('thursdayTime'))
        fridayTime = json.dumps(request.form.getlist('fridayTime'))
        saturdayTime = json.dumps(request.form.getlist('saturdayTime'))
        sundayTime = json.dumps(request.form.getlist('sundayTime'))
        tutorName = json.dumps(request.form.getlist('tutor'))

        tuesday = json.dumps(request.form.get('Tuesday'))

        # print(tuesday)

        tutorApptInfoTemp = tutorName
        tutorApptInfoArr = tutorApptInfoTemp.split(' ')
        tutorApptInfo = tutorApptInfoArr[1] + ' ' + \
            tutorApptInfoArr[2] + ' ' + tutorApptInfoArr[3].split('"')[0]

        tutorftemp = tutorName.split('/ ')
        tutorfirstName = tutorftemp[1].split('"')

        tutorID = Tutor.query.filter_by(first_name=tutorfirstName[0]).first()
        tutorIDString = str(tutorID)
        tutorIDNum = tutorIDString[7]

        try:
            studentftemp = str(current_user)
            studentidtemp = studentftemp.split(' ')
            studentIDtemp = studentidtemp[1].split('>')
            studentID = studentIDtemp[0]
        except:
            print('')

        weekdayNum = datetime.datetime.today().weekday()

        if weekdayNum != 4:
            newweekdayNum = datetime.datetime.today().weekday()
            offset = abs(newweekdayNum - weekdayNum)
        else:
            offset = 0

        timesArr = [mondayTime, tuesdayTime, wednesdayTime,
                    thursdayTime, fridayTime, saturdayTime, sundayTime]

        for i in range(len(timesArr)):
            if timesArr[i] == "[]":
                pass
            else:
                time = timesArr[i]
                weekday = i + 1

        # print(time, weekday)

        if weekday == 1:
            apptDate = date.today()
        elif weekday == 2:
            apptDate = date.today() + timedelta(1 + offset)
        elif weekday == 3:
            apptDate = date.today() + timedelta(2 + offset)
        elif weekday == 4:
            apptDate = date.today() + timedelta(3 + offset)
        elif weekday == 5:
            apptDate = date.today() + timedelta(4 + offset)
        elif weekday == 6:
            apptDate = date.today() + timedelta(5 + offset)
        elif weekday == 7:
            apptDate = date.today() + timedelta(6 + offset)

        print(apptDate)

        print('Creating appointment')
        new_appointment = Appointment(date=apptDate, time=time, student_id=studentID,
                                      tutor_id=tutorIDNum, appointment_info=tutorApptInfo, zoom_link='xyz')
        db.session.add(new_appointment)
        db.session.commit()
        print('Appointment Created')
        flash('Appointment created!', category='success')
        return redirect(url_for('views.apptCreated'))

    my_date = date.today()
    day = calendar.day_name[my_date.weekday()]
    print(day)

    weekdayNum = datetime.datetime.today().weekday()

    if weekdayNum != 4:
        newweekdayNum = datetime.datetime.today().weekday()
        offset = abs(newweekdayNum - weekdayNum)
    else:
        offset = 0

    today = date.today()
    tomorrow = date.today() + timedelta(1 + offset)
    twoDays = date.today() + timedelta(2 + offset)
    threeDays = date.today() + timedelta(3 + offset)
    fourDays = date.today() + timedelta(4 + offset)
    fiveDays = date.today() + timedelta(5 + offset)
    sixDays = date.today() + timedelta(6 + offset)
    sevenDays = date.today() + timedelta(7 + offset)

    our_tutors = Tutor.query.order_by(Tutor.id)

    return render_template("make-appointment.html", our_tutors=our_tutors, user=current_user, today=today, tomorrow=tomorrow, twoDays=twoDays, threeDays=threeDays, fourDays=fourDays, fiveDays=fiveDays, sixDays=sixDays, sevenDays=sevenDays)
