from flask import Blueprint, render_template, request, url_for
from .models import *

views = Blueprint('views', __name__)

@views.route('/')
def index():
    tutor_search = request.args.get('tutor_search')
    if tutor_search:
        tutor_all = Tutor.query.filter(Tutor.first_name.contains(tutor_search) | Tutor.last_name.contains(tutor_search) | Tutor.id.contains(tutor_search))
    else:
        tutor_all = Tutor.query.all()
    return render_template('index.html', tutor_all=tutor_all)

@views.route('/userHome')
def userHome():
    tutor_search = request.args.get('tutor_search')
    if tutor_search:
        tutor_all = Tutor.query.filter(Tutor.first_name.contains(tutor_search) | Tutor.last_name.contains(tutor_search) | Tutor.id.contains(tutor_search))
    else:
        tutor_all = Tutor.query.all()
    return render_template('userHome.html', tutor_all=tutor_all)

@views.route('/tutorHome')
def tutorHome():
    return render_template('tutorHome.html')