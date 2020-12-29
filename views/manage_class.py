from flask import Blueprint, request, jsonify, abort, session, render_template, current_app

from common.Role import *
from decorators import should_be, login_required
from models import Mentor, Student, Course

class_bp = Blueprint('class_bp', __name__)


def has_this_class(cno):
    role = session.get('role')
    if role == STUDENT:
        if_has = Student.has_this_class(session['no'], cno)
    elif role == MENTOR:
        if_has = Mentor.has_this_class(session['no'], cno)
    else:
        if_has = False

    return if_has


@class_bp.route('/')
def get_class():
    return current_app.send_static_file('html/test_stat.html')


@class_bp.route('/list')
@login_required('json')
def get_classes():
    """
    返回全部班级的信息
    """
    if session['role'] == STUDENT:
        classes = Student.get_classes(session['no'])
    elif session['role'] == MENTOR:
        classes = Mentor.get_classes(session['no'])
    else:
        return jsonify({'code': 403})

    res_json = {'code': 200, 'classes': []}
    res_classes = res_json['classes']

    for cur_cls in classes:
        res_classes.append({
            'cno': cur_cls.Cno,
            'cname': cur_cls.Cname,
            'csubject': cur_cls.Csubject
        })

    return jsonify(res_json)


@class_bp.route('/detail')
@login_required('redirect')
def get_exam_list_page():
    cno = request.args.get('cno')
    if cno is None:
        abort(404)
    cno = int(cno)

    if not has_this_class(cno):
        abort(404)

    return render_template('test_list.html')


@class_bp.route('/member', methods=['GET'])
@login_required('json')
def get_class_member():
    cno = request.args.get('cno')
    if cno is None:
        abort(404)
    cno = int(cno)

    if not has_this_class(cno):
        abort(404)

    members = Course.get_students_by_no(cno)
    res_json = {'code': 200, 'members': []}
    res_members = res_json['members']
    for member in members:
        res_members.append({
            'sno': member.Sno,
            'sname': member.Sname
        })

    return jsonify(res_json)


@class_bp.route('/member', methods=['POST', 'DELETE'])
@should_be([MENTOR])
def change_student():
    cno = int(request.form['cno'])
    sno = int(request.form['sno'])

    if not Mentor.has_this_class(session['no'], cno):
        return jsonify({'code': 204})

    if request.method == 'POST':
        flag = Course.add_class_member(cno, sno)
        if not flag:
            # 学生已存在
            return jsonify({'code': 203})
        return jsonify({'code': 200})

    elif request.method == 'DELETE':
        flag = Course.del_class_member(cno, sno)
        if not flag:
            # 学生不存在
            return jsonify({'code': 204})
        return jsonify({'code': 200})


@class_bp.route('stat')
def get_exam_stat():
    cno = request.args.get('cno')
    if cno is None or not has_this_class(int(cno)):
        abort(404)

    return render_template('test_stat.html')
