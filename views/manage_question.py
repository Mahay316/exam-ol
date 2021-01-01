from flask import Blueprint, request, jsonify, session, current_app, abort
from models import Question
from common.Role import *
from decorators import should_be, login_required
from math import ceil
from config import PAGE_SIZE

question_bp = Blueprint('question_bp', __name__)


@question_bp.route('/manage')
@login_required('redirect')
def question_index():
    if session['role'] == MENTOR:
        return current_app.send_static_file('html/question_repo.html')
    else:
        abort(404)


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

    qsubject = int(qsubject)

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
    subject, qtype, content, page = None, None, None, 1
    subject = args.get('subject')
    qtype = args.get('type')
    content = args.get('content')
    page = args.get('page')

    if page is None:
        page = 1

    res_json = {'code': 200, 'questions': []}
    select_dict = {}

    if subject is not None:
        select_dict['subject'] = int(subject)
        # results = Question.select_questions_by(page, subject=subject)
    elif qtype is not None:
        select_dict['qtype'] = qtype
        # results = Question.select_questions_by(page, qtype=qtype)
    # elif qno is not None:
    #     results = Question.select_questions_by(page, qno=qno)
    elif content is not None:
        select_dict['content'] = content
        # results = Question.select_questions_by(page, content=content)

    results = Question.select_questions_by(int(page), **select_dict)

    for result in results:
        res_json['questions'].append({
            'qno': result.Qno,
            'qtype': result.Qtype,
            'qstem': result.Qstem,
            'qselect': result.Qselect,
            'qanswer': result.Qanswer,
            'qsubject': result.Subno
        })

    num = len(results)
    res_json['page_num'] = ceil(num / PAGE_SIZE)
    res_json['info_num'] = num

    return jsonify(res_json)


@question_bp.route('/', methods=['DELETE'])
@should_be([MENTOR])
def delete_question():
    """
    删除试题
    """
    qno = int(request.args['qno'])
    Question.delete_question(qno)
    return jsonify({'code': 200})


@question_bp.route('/', methods=['PUT'])
@should_be([MENTOR])
def update_question():
    """
    更新试题
    """
    args = request.args
    qno = int(args['qno'])
    qtype = args['qtype']
    qstem = args['qstem']
    qanswer = args['qanswer']
    qselect = args['qselect']
    qsubject = int(args['qsubject'])
    Question.update_question(qno, qtype, qstem, qanswer, qselect, qsubject)
    return jsonify({'code': 200})


@question_bp.route('/page_num')
def get_question_page_num():
    num = Question.get_question_num()
    return jsonify({
        'code': 200,
        'page_num': ceil(num / PAGE_SIZE),
        'info_num': num
    })
