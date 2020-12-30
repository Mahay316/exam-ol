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


@student_bp.route('/')
@should_be([MENTOR])
def get_students():
    args = request.args
    no = args.get('no')
    name = args.get('name')
    major = args.get('major')
    page = args.get('page')

    if page is None:
        page = 1

    res_json = {'code': 200, 'students': []}

    select_dict = {}
    if no is not None:
        select_dict['no'] = no
        # results = Paper.select_papers_by(page, subject=subject)
    elif major is not None:
        select_dict['major'] = major
        # results = Paper.select_papers_by(page, used=used)
    elif name is not None:
        select_dict['name'] = name
        # results = Paper.select_papers_by(page, pno=pno)
    num, results = Student.select_students_by(int(page), **select_dict)

    for result in results:
        res_json['students'].append({
            'no': result.Sno,
            'name': result.Sname,
            'gender': result.Sgender,
            'major': result.Smajor,
        })

    res_json['page_num'] = ceil(num / PAGE_SIZE)
    res_json['info_num'] = num

    return jsonify(res_json)

