from flask import Blueprint, render_template, session, flash, request, url_for, redirect
from models.UserModel import User, Mentor, Student, Admin
from common import save_session
from common.Role import *

auth = Blueprint('auth', __name__)


@auth.route('/login', method=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        role = request.form['role']
        if role == STUDENT:
            user = Student.get_user(username)
        elif role == MENTOR:
            user = Mentor.get_user(username)
        elif role == ADMIN:
            user = Admin.get_user(username)

        if user is not None and user.verify_password(password):
            remember_me = request.form['remember_me']

            save_session(role, user, remember_me)

            # resp = redirect(next_url)
            # if remember_me:
            #     resp.set_cookie('username', username)
            #     resp.set_cookie('password', password)
            #     resp.set_cookie('role', role)

            return redirect(url_for('login'))

    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.permanent = False
    session.clear()

    # resp = redirect(from_url)
    #
    # resp.delete_cookie('username')
    # resp.delete_cookie('password')
    # resp.delete_cookie('role')

    return redirect(url_for('login'))
