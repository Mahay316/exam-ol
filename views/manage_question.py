from flask import Blueprint, request, jsonify, session, redirect, url_for, abort, render_template
from models import Question
from common.Role import *
from decorators import should_be, login_required

question_bp = Blueprint('question_bp', __name__)


@question_bp.route('/', methods=['POST'])
@should_be([MENTOR])
def add_question():
    """
    向试卷库添加question
    """
    form = request.form
    filed = ['code', 'qtype', 'qstem', 'qanswer', 'qselect', 'qsubject']
    try:
        code, qtype, qstem, qanswer, qselect, qsubject = list(map(lambda x: form[x], filed))
    except:
        return jsonify({'code': 204})

    flag = Question.add_question(qtype, qstem, qanswer, qselect, qsubject)
    if flag:
        return jsonify({'code': 200})
    return jsonify({'code': 403})


@question_bp.route('/', methods=['GET'])
@should_be([MENTOR])
def get_questions():
    """
    根据筛选条件返回筛选出的试题
    """
    args = request.args
    subject, qtype, qno, content, page = None, None, None, None, 1
    subject = args.get('subject')
    qtype = args.get('type')
    qno = args.get('qno')
    content = args.get('content')
    page = args.get('page')

    res_json = {'code': 200, 'questions': []}

    if subject is not None:
        results = Question.select_questions_by(page, subject=subject)
    elif qtype is not None:
        results = Question.select_questions_by(page, qtype=qtype)
    elif qno is not None:
        results = Question.select_questions_by(page, qno=qno)
    elif content is not None:
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


@question_bp.route('/manage')
@login_required('redirect')
def question_index():
    if session['role'] == MENTOR:
        return render_template('question_repo.html')
    else:
        abort(404)
