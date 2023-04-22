from flask import Blueprint, render_template, request, url_for
from flask_login import login_required, current_user
from .models import *

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

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
    # tutor_search = request.args.get('tutor_search')
    # if tutor_search:
    #     tutor_all = Tutor.query.filter(Tutor.first_name.contains(tutor_search) | Tutor.last_name.contains(tutor_search) | Tutor.id.contains(tutor_search))
    # else:
    #     tutor_all = Tutor.query.all()


    return render_template('student-home.html', user=current_user)#tutor_all=tutor_all

@views.route('/tutor')
@login_required
def tutor_home():
    return render_template('tutor-home.html', user=current_user)
