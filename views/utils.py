from flask import jsonify, Blueprint, request, jsonify, session, redirect, url_for, abort, render_template
from models import Test, Student, Mentor
from datetime import datetime
from common.Role import *
from decorators import should_be

utils_bp = Blueprint('utils_bp', __name__)


@utils_bp.route('/get_classes')
def get_classes():
    """
    返回全部班级的信息
    教师和学生在'{role}/class'页面均请求该接口
    """
    if 'role' not in session:
        abort(404)

    if session['role'] == STUDENT:
        classes = Student.get_classes(session['no'])
    elif session['role'] == MENTOR:
        classes = Mentor.get_classes(session['no'])
    else:
        abort(404)

    res_json = {'code': 200, 'classes': []}
    res_classes = res_json['classes']

    for cur_cls in classes:
        res_classes.append({
            'cno': cur_cls.Cno,
            'cname': cur_cls.Cname,
            'csubject': cur_cls.Csubject
        })

    return jsonify(res_json)