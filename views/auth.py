from flask import Blueprint, current_app, session, jsonify, request, url_for, redirect
from models.UserModel import Mentor, Student, Admin
from common import save_session
from common.Role import *

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'role' in session:
        # TODO 用户已经登录过如何处理
        return redirect(url_for('index'))

    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        role = request.form['role']
        user = None
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

            return jsonify({'code': 200})
        # 登录失败
        return jsonify({'code': 403})

    return current_app.send_static_file('html/login.html')


@auth_bp.route('/logout', methods=['POST'])
def logout():
    if 'role' not in session:
        return jsonify({'code': 403})

    session.permanent = False
    session.clear()

    # resp = redirect(from_url)
    #
    # resp.delete_cookie('username')
    # resp.delete_cookie('password')
    # resp.delete_cookie('role')

    return jsonify({'code': 200})


@auth_bp.route('/info', methods=['GET'])
def get_info():
    if 'role' not in session:
        return jsonify({'code': 403})

    role = session['role']
    res_json = {'code': 200, 'no': session['no'], 'role': role}
    if role == STUDENT:
        res_json['name'] = session['name']
        res_json['gender'] = session['gender']
        res_json['major'] = session['major']
    elif role == MENTOR:
        res_json['name'] = session['name']
        res_json['gender'] = session['gender']
        res_json['title'] = session['title']
    elif role == ADMIN:
        res_json['name'] =session['no']
    return jsonify(res_json)
