from flask import jsonify, Blueprint, request, jsonify, session, redirect, url_for, abort, render_template
from models import Test, Student, Mentor, Paper
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
        abort(403)

    if session['role'] == STUDENT:
        classes = Student.get_classes(session['no'])
    elif session['role'] == MENTOR:
        classes = Mentor.get_classes(session['no'])
    else:
        abort(403)

    res_json = {'code': 200, 'classes': []}
    res_classes = res_json['classes']

    for cur_cls in classes:
        res_classes.append({
            'cno': cur_cls.Cno,
            'cname': cur_cls.Cname,
            'csubject': cur_cls.Csubject
        })

    return jsonify(res_json)


@utils_bp.route('/get_papers')
@should_be([MENTOR, STUDENT])
def get_papers():
    """
    获取全部考试

    :return: json
    """
    papers = Paper.get_all_papers()

    res_json = {'code': 200, 'papers': []}
    res_papers = res_json['papers']

    for paper in papers:
        res_papers.append({
            'pno': paper.Cno,
            'pname': paper.Cname,
            'psubject': paper.Csubject
        })

    return jsonify(res_json)