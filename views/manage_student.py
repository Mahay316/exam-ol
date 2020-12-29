from flask import Blueprint, request, jsonify, session, current_app, abort
from models import Student
from common.Role import *
from decorators import should_be, login_required
from math import ceil
from config import PAGE_SIZE

student_bp = Blueprint('student_bp', __name__)


@student_bp.route('/search')
@should_be([MENTOR, ADMIN])
def search_student():
    cno = int(request.args['cno'])
    sno = request.args['sno']

    # TODO 204
    student = Student.get_user(sno)
    res_json = {
        'code': 200,
        'sno': student.Sno,
        'sname': student.Sname,
        'in_class': Student.has_this_class(sno, cno)
    }

    return jsonify(res_json)
