from flask import Blueprint, request, jsonify, session, redirect, url_for, abort, render_template
from models import Class, Mentor, StudentTest, Question
from common.Role import *
from decorators import should_be

mentor_bp = Blueprint('mentor_bp', __name__)


@mentor_bp.route('/class/<string:class_id>', methods=['GET', 'POST'])
@should_be([MENTOR])
def class_management(class_id: str):
    """
    班级信息管理

    - GET方法返回html，用jinja后端渲染学生信息和考试下拉列表
    - POST方法给出考试id，返回考试统计结果
    """
    if not Mentor.has_this_class(session['no'], class_id):
        abort(403)

    if request.method == 'GET':
        # GET中使用jinja直接渲染试题列表和学生信息列表
        tests = Class.get_tests_by_no(class_id)
        students = Class.get_students_by_no(class_id)

        return render_template('class_manage.html', tests=tests, students=students)
    elif request.method == 'POST':
        test_no = request.form.get('test_no')
        if test_no is None:
            abort(403)

        results = StudentTest.get_st_by_tno(test_no)
        res_json = {'code': 200, 'results': results}
        return jsonify(res_json)


@mentor_bp.route('/get_questions', methods=['POST'])
@should_be([MENTOR])
def get_questions():
    """
    根据筛选条件返回筛选出的试题
    """
    form = request.form
    # TODO 无法记录筛选时的条件，分页会出错
    subject, qtype, qno, content, page = '', '', '', '', 1
    try:
        subject = form['subject']
        qtype = form['type']
        qno = form['qno']
        content = form['content']
        page = form['page']
    except Exception:
        abort(404)

    res_json = {'code': 200, 'questions':[]}

    if subject != '':
        results = Question.select_questions_by(page, subject=subject)
    elif qtype != '':
        results = Question.select_questions_by(page, qtype=qtype)
    elif qno != '':
        results = Question.select_questions_by(page, qno=qno)
    elif content != '':
        results = Question.select_questions_by(page, content=content)
    else:
        results = Question.select_questions_by(page)

    for result in results:
        res_json['questions'].append({
            'qno': result.Qno,
            'qtype': result.Qtype,
            'qstem': result.Qstem,
            'qselect': result.Qselect,
            'qanswer': result.Qanswer,
            'qsubject': result.Qsubject
        })

    return jsonify(res_json)
