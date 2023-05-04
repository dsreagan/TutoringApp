from flask import Blueprint, render_template, request, url_for
from flask_login import login_required, current_user
from .models import *
import json

views = Blueprint('views', __name__)

@views.route('/')
def index():
    tutor_search = request.args.get('tutor_search')
    if tutor_search:
        tutor_all = Tutor.query.filter(Tutor.first_name.contains(tutor_search) | Tutor.last_name.contains(tutor_search) | Tutor.id.contains(tutor_search) | Tutor.subjects.contains(tutor_search)).all()
    else:
        tutor_all = Tutor.query.all()
    return render_template('index.html', user=current_user, tutor_all=tutor_all)

@views.route('/student')
@login_required
def student_home():
    tutor_search = request.args.get('tutor_search')
    if tutor_search:
        tutor_all = Tutor.query.filter(Tutor.first_name.contains(tutor_search) | Tutor.last_name.contains(tutor_search) | Tutor.id.contains(tutor_search) | Tutor.subjects.contains(tutor_search)).all()
    else:
        tutor_all = Tutor.query.all()
    return render_template('student-home.html', user=current_user, tutor_all=tutor_all)

@views.route('/tutor')
@login_required
def tutor_home():
    return render_template('tutor-home.html', user=current_user)

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
