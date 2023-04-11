from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p>Login</p>"

@auth.route('/signup')
def signup():
    return "<p>Signup</p>"

@auth.route('/tutorRegistration', methods=['GET', 'POST'])
def tutorRegistration():
    return render_template('tutorRegistration.html')