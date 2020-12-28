from flask import Blueprint, request, jsonify, session, redirect, url_for, abort, render_template
from models import Class, Mentor, StudentTest, Question
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


@question_bp.route('/manage')
@login_required('redirect')
def question_index():
    if session['role'] == MENTOR:
        return render_template('question_repo.html')
    else:
        abort(404)