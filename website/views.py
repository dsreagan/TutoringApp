from flask import Blueprint, render_template, request, url_for
from flask_login import login_required, current_user
from .models import *
import mimetypes
import base64
import io

views = Blueprint('views', __name__)

@views.route('/')
def index():
    tutor_search = request.args.get('tutor_search')
    if tutor_search:
        tutor_all = Tutor.query.filter(Tutor.first_name.contains(tutor_search) | Tutor.last_name.contains(tutor_search) | Tutor.id.contains(tutor_search) | Tutor.subjects.contains(tutor_search)).all()
    else:
        tutor_all = Tutor.query.all()
    return render_template('index.html', user=current_user, tutor_all=tutor_all)

@views.route('/registered')
def registered():
    return render_template('registered.html', user=current_user)

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
    user_id = current_user.id
    user_row = Tutor.query.filter_by(id=user_id).first()
    binary_data = user_row.profile_pic
    file_obj = io.BytesIO(binary_data)
    decoded_data = base64.b64encode(file_obj.read()).decode('utf-8')
    file_type, encoding = mimetypes.guess_type(user_row.profile_picname)
    return render_template('tutor-home.html', user=current_user, data=decoded_data, fileType = file_type)
