from flask import Blueprint, request, jsonify, session, redirect, url_for, abort, render_template
from models import Test
from datetime import datetime
from common.Role import *
from decorators import should_be

utils_bp = Blueprint('utils_bp', __name__)


@utils_bp.route('/get_classes')
def get_classes():
    """
    返回全部班级的信息
    教师和学生在'{role}/class'页面均请求该接口
    """
    if 'role' not in session:
        abort(404)

    if session['role'] == STUDENT:
        pass
    elif session['role'] == MENTOR:
        pass
    else:
        abort(404)