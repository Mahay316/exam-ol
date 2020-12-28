from flask import Blueprint, request, jsonify, session, redirect, url_for, abort, render_template
from models import Paper
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
        return render_template('paper_repo.html')
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

    res_json = {'code': 200, 'questions': []}

    select_dict = {}
    if subject is not None:
        select_dict['subject'] = subject
        # results = Paper.select_papers_by(page, subject=subject)
    elif used is not None:
        select_dict['used'] = used
        # results = Paper.select_papers_by(page, used=used)
    elif pno is not None:
        select_dict['pno'] = pno
        # results = Paper.select_papers_by(page, pno=pno)
    elif pname is not None:
        select_dict['pname'] = pname
        # results = Paper.select_papers_by(page, pname=pname)
    results = Paper.select_papers_by(page, **select_dict)

    for result in results:
        res_json['questions'].append({
            'pno': result.Pno,
            'pname': result.Pname,
            'preferenced': result.Preferenced,
            'psubject': result.psubject
        })

    return jsonify(res_json)


@paper_bp.route('/', methods=['POST'])
@should_be([MENTOR])
def add_paper():
    form = request.form
    questions = form.get('questions')
    pname = form.get('pname')
    subno = form.get('subno')

    questions = json.loads(questions)
    flag = Paper.add_paper(questions, pname, subno)

    if flag:
        return jsonify({'code': 200})
    return jsonify({'code': 403})


@paper_bp.route('/', methods=['DELETE'])
@should_be([MENTOR])
def delete_paper():
    pno = request.form['DELETE']
    Paper.delete_paper(pno)
    return jsonify({'code': 200})


@paper_bp.route('/preview', methods=['GET', 'POST'])
@should_be([MENTOR])
def preview_paper():
    """
    预览试卷。POST方法用于正在组卷的预览，GET用于预览已存在的卷子
    """
    if request.method == 'GET':
        pno = request.args['pno']
        paper = Paper.select_papers_by(1, pno=pno)
        res_json = {}
    # TODO to implement
    else:
        pass


@paper_bp.route('page_num')
@should_be([MENTOR])
def get_paper_page_num():
    return jsonify({
        'code': 200,
        'page_num': ceil(Paper.get_paper_num() / PAGE_SIZE)
    })
