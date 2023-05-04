from flask import Blueprint, render_template, request, url_for
from flask_login import login_required, current_user
from .models import *
import mimetypes
import base64
import io
from . import db
import json


views = Blueprint('views', __name__)

@views.route('/')
def index():
    tutor_search = request.args.get('tutor_search')
    if tutor_search:
        tutor_all = Tutor.query.filter(Tutor.first_name.contains(tutor_search) | Tutor.last_name.contains(tutor_search) | Tutor.id.contains(tutor_search) | Tutor.subjects.contains(tutor_search)).all()
    else:
        tutor_all = Tutor.query.all()
    for tutor in tutor_all:
        user_id = tutor.id
        user_row = Tutor.query.filter_by(id=user_id).first()
        binary_data = user_row.profile_pic
        file_obj = io.BytesIO(binary_data)
        decoded_data = base64.b64encode(file_obj.read()).decode('utf-8')
        file_type, encoding = mimetypes.guess_type(user_row.profile_picname)
    
    return render_template('index.html', user=current_user, tutor_all=tutor_all, data=decoded_data, fileType = file_type)


@views.route('/student')
@login_required
def student_home():

    appts_Table = request.args.get('appt_Table')
    appt_found = Appointment.query.join(Tutor, Tutor.id == Appointment.tutor_id).filter(Appointment.student_id == current_user.get_id())
    #print(current_user.get_id())
    #print(appt_found)
    tutorNames_found = Tutor.query.join(Appointment, Tutor.id == Appointment.tutor_id).filter(Appointment.student_id == current_user.get_id()).all()
    #print(tutorNames_found)
    JoinedRows = []
    for appt in appt_found:
        for tutor in tutorNames_found:
            if tutor.id == appt.tutor_id:
                JoinedRows.append([appt, str(tutor.first_name + ' ' + tutor.last_name)])

    tutor_search = request.args.get('tutor_search')
    if tutor_search:
        tutor_all = Tutor.query.filter(Tutor.first_name.contains(tutor_search) | Tutor.last_name.contains(tutor_search) | Tutor.id.contains(tutor_search))
    else:
        tutor_all = Tutor.query.all()
    
    for tutor in tutor_all:
        user_id = tutor.id
        user_row = Tutor.query.filter_by(id=user_id).first()
        binary_data = user_row.profile_pic
        file_obj = io.BytesIO(binary_data)
        decoded_data = base64.b64encode(file_obj.read()).decode('utf-8')
        file_type, encoding = mimetypes.guess_type(user_row.profile_picname)
    
    return render_template('student-home.html', user=current_user, tutor_all=tutor_all, data=decoded_data, fileType = file_type, appointments=JoinedRows)


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
    appt_found = Appointment.query.join(Tutor, Tutor.id == Appointment.tutor_id).filter(Appointment.tutor_id == current_user.get_id())
    print(current_user.get_id())
    print(appt_found)
    studentNames_found = Student.query.join(Appointment, Student.id == Appointment.student_id).filter(Appointment.tutor_id == current_user.get_id()).all()
    print(studentNames_found)
    JoinedRows = []
    for appt in appt_found:
        for student in studentNames_found:
            if student.id == appt.student_id:
                JoinedRows.append([appt, str(student.first_name + ' ' + student.last_name)])

    return render_template('tutor-home.html', user=current_user, appointments = JoinedRows, data=decoded_data, fileType = file_type)
    

@views.route('/appointments', methods=['GET', 'POST'])
def make_appointment():
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

    return render_template("make-appointment.html", user=current_user, our_tutors=our_tutors)