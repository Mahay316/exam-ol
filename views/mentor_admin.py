from flask import Blueprint, request, jsonify, session, redirect, url_for, abort, render_template
from models import Class, Mentor
from datetime import datetime
from common.Role import *
from decorators import should_be
import json

mentor_bp = Blueprint('mentor_bp', __name__)


# @mentor_bp.route('/class')
# @should_be([MENTOR])
# def teacher_admin():
#     """
#     展示全部班级
#
#     :return html页面
#     """
#


@mentor_bp.route('/class/<string:class_id>', methods=['GET', 'POST'])
@should_be([MENTOR])
def class_management(class_id: str):
    """
    班级信息管理

    - GET方法返回html，用jinja后端渲染学生信息和考试下拉列表
    - POST方法给出考试id，返回考试统计结果
    """
    if not Mentor.has_this_class(session['no'], class_id):
        abort(404)

    if request.method == 'GET':
        # GET中使用jinja直接渲染试题列表和学生信息列表
        tests = Class.get_tests_by_no(class_id)
        students = Class.get_students_by_no(class_id)

        return render_template('class_manage.html', tests=tests, students=students)
    elif request.method == 'POST':
        pass
