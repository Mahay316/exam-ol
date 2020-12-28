from flask import Blueprint, request, jsonify, session, redirect, url_for, abort, render_template
from models import Class, Mentor, StudentTest, Question
from common.Role import *
from decorators import should_be, login_required

question_bp = Blueprint('question_bp', __name__)


@question_bp.route('/manage')
@login_required('redirect')
def question_index():
    if session['role'] == MENTOR:
        return render_template('question_repo.html')
    else:
        abort(404)