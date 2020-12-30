from flask import Blueprint, request, jsonify, current_app
from models import Mentor
from common.Role import *
from decorators import should_be
from config import PAGE_SIZE
from math import ceil

mentor_bp = Blueprint('mentor_bp', __name__)


@mentor_bp.route('/manage', methods=['GET'])
@should_be([ADMIN])
def get_manage_mentor_page():
    return current_app.send_static_file('html/admin.html')


@mentor_bp.route('/', methods=['GET'])
@should_be([ADMIN])
def get_mentors():
    args = request.args
    no = args.get('no')
    title = args.get('title')
    name = args.get('name')
    page = args.get('page')

    if page is None:
        page = 1

    res_json = {'code': 200, 'mentors': []}

    select_dict = {}
    if no is not None:
        select_dict['no'] = no
        # results = Paper.select_papers_by(page, subject=subject)
    elif title is not None:
        select_dict['title'] = title
        # results = Paper.select_papers_by(page, used=used)
    elif name is not None:
        select_dict['name'] = name
        # results = Paper.select_papers_by(page, pno=pno)
    results = Mentor.select_mentors_by(int(page), **select_dict)

    for result in results:
        res_json['mentors'].append({
            'no': result.Mno,
            'name': result.Mname,
            'title': result.Mtitle,
            'gender': result.Mgender,
        })

    num = len(results)
    res_json['page_num'] = ceil(num / PAGE_SIZE)
    res_json['info_num'] = num

    return jsonify(res_json)
