from flask import Blueprint, render_template, request, url_for
from flask_login import login_required, current_user
from .models import *
from . import db


views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html', user=current_user)

@views.route('/registered')
def registered():
    return render_template('registered.html')

    tutor_search = request.args.get('tutor_search')
    if tutor_search:
        tutor_all = Tutor.query.filter(Tutor.first_name.contains(tutor_search) | Tutor.last_name.contains(tutor_search) | Tutor.id.contains(tutor_search))
    else:
        tutor_all = Tutor.query.all()
    return render_template('index.html', tutor_all=tutor_all)

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


    return render_template('student-home.html', user=current_user, tutor_all=tutor_all, appointments=JoinedRows)

@views.route('/tutor')
@login_required
def tutor_home():
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


    return render_template('tutor-home.html', user=current_user, appointments = JoinedRows)
