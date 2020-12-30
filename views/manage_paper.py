from flask import Blueprint, request, current_app, jsonify, session, redirect, url_for, abort
from models import Paper, Question
from common.Role import *
from decorators import should_be, login_required
import json
from config import PAGE_SIZE
from math import ceil

paper_bp = Blueprint('paper_bp', __name__)


@paper_bp.route('/manage')
@login_required('redirect')
def paper_index():
    if session['role'] == MENTOR:
        return current_app.send_static_file('html/paper_repo.html')
    else:
        abort(404)


@paper_bp.route('/', methods=['GET'])
@should_be([MENTOR])
def get_paper():
    args = request.args
    subject = args.get('subject')
    used = args.get('used')
    pno = args.get('pno')
    pname = args.get('pname')
    page = args.get('page')

    if page is None:
        page = 1

    res_json = {'code': 200, 'papers': []}

    select_dict = {}
    if subject is not None:
        select_dict['subject'] = int(subject)
        # results = Paper.select_papers_by(page, subject=subject)
    elif used is not None:
        select_dict['used'] = True if used == 'true' else False
        # results = Paper.select_papers_by(page, used=used)
    elif pno is not None:
        select_dict['pno'] = pno
        # results = Paper.select_papers_by(page, pno=pno)
    elif pname is not None:
        select_dict['pname'] = pname
        # results = Paper.select_papers_by(page, pname=pname)
    results = Paper.select_papers_by(int(page), **select_dict)

    for result in results:
        res_json['papers'].append({
            'pno': result.Pno,
            'pname': result.Pname,
            'preference': True if result.Preference > 0 else False,
            'psubject': result.Subno
        })

    num = Paper.get_paper_num()
    res_json['page_num'] = ceil(num / PAGE_SIZE)
    res_json['info_num'] = num

    return jsonify(res_json)


@paper_bp.route('/', methods=['POST'])
@should_be([MENTOR])
def add_paper():
    form = request.form
    questions = form.get('questions')
    pname = form.get('pname')
    subno = int(form.get('subno'))

    questions = json.loads(questions)
    flag = Paper.add_paper(questions, pname, subno)

    if flag:
        return jsonify({'code': 200})
    return jsonify({'code': 403})


@paper_bp.route('/', methods=['DELETE'])
@should_be([MENTOR])
def delete_paper():
    pno = int(request.args['pno'])
    Paper.delete_paper(pno)
    return jsonify({'code': 200})


@paper_bp.route('/preview', methods=['GET', 'POST'])
@should_be([MENTOR])
def preview_paper():
    """
    预览试卷。POST方法用于正在组卷的预览，GET用于预览已存在的卷子
    """
    if request.method == 'GET':
        pno = int(request.args['pno'])
        res_json = {
            'code': 200,
            'questions': []
        }

        questions = Question.get_questions_by_pno(pno)
        for q in questions:
            res_json['questions'].append({
                'qno': q.Qno,
                'qtype': q.Qtype,
                'qstem': q.Qstem,
                'qanswer': q.Qanswer,
                'qselect': q.Qselect
            })

        return jsonify(res_json)
    else:
        # TODO 用于正在组卷的预览
        pass


@paper_bp.route('/page_num')
@should_be([MENTOR])
def get_paper_page_num():
    num = Paper.get_paper_num()
    return jsonify({
        'code': 200,
        'page_num': ceil(num / PAGE_SIZE),
        'info_num': num
    })


@paper_bp.route('/assemble')
@should_be([MENTOR])
def add_paper_page():
    return paper_bp.send_static_file('html/paper_assemble.html')
