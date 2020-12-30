from flask import Blueprint, request, jsonify, session, current_app, abort
from models import Mentor
from common.Role import *
from decorators import should_be, login_required

mentor_bp = Blueprint('mentor_bp', __name__)


@mentor_bp.route('/manage', method=['GET'])
@should_be([ADMIN])
def get_manage_mentor_page():
    return current_app.send_static_file('html/admin.html')


@mentor_bp.route('/', methods=['GET'])
def get_mentors():
    args = request.args
    no = args.get('no')
    title = args.get('title')
    name = args.get('name')
    page = args.get('page')

    if page is None:
        page = 1

    res_json = {'code': 200, 'students': []}

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
