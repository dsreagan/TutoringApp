from flask import Blueprint, render_template
from .models import *

views = Blueprint('views', __name__)

@views.route('/')
def index():
    tutor_all = Tutor.query.all()
    return render_template('index.html', tutor_all=tutor_all)