from flask import Blueprint, request, jsonify, session, redirect, url_for, abort, render_template
from models import Question
from common.Role import *
from decorators import should_be, login_required

paper_bp = Blueprint('paper_bp', __name__)


@paper_bp.route('/manage')
@login_required('redirect')
def paper_index():
    if session['role'] == MENTOR:
        return render_template('paper_repo.html')
    else:
        abort(404)


@paper_bp.route('/get_questions', methods=['POST'])
@should_be([MENTOR])
def get_questions():
    """
    根据筛选条件返回筛选出的试题
    """
    form = request.form
    subject, qtype, qno, content, page = '', '', '', '', 1
    try:
        subject = form['subject']
        qtype = form['type']
        qno = form['qno']
        content = form['content']
        page = form['page']
    except Exception:
        return jsonify({'code': 403})

    res_json = {'code': 200, 'questions': []}

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
