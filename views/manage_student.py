from flask import Blueprint, request, jsonify, session, current_app, abort
from models import Student
from common.Role import *
from decorators import should_be, login_required
from math import ceil
from config import PAGE_SIZE

student_bp = Blueprint('student_bp', __name__)


@student_bp.route('/manage', methods=['GET'])
@should_be([ADMIN])
def get_student_manage_page():
    return current_app.send_static_file('html/admin.html')


@student_bp.route('/', methods=['POST'])
@should_be([ADMIN])
def add_student():
    """增加学生"""


@student_bp.route('/', methods=['GET'])
@should_be([ADMIN])
def get_students():
    pass


@student_bp.route('/search')
@should_be([MENTOR, ADMIN])
def search_student():
    cno = int(request.args['cno'])
    sno = request.args['sno']

    student = Student.get_user(sno)

    if student is None:
        return jsonify({'code': 204})

    res_json = {
        'code': 200,
        'sno': student.Sno,
        'sname': student.Sname,
        'in_class': Student.has_this_class(sno, cno)
    }

    return jsonify(res_json)
