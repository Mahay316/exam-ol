from flask import Blueprint, request, jsonify, session, redirect, url_for, abort
from models import Test
from datetime import datetime
from common.Role import *
import json

index_bp = Blueprint('index_bp', __name__)

@index_bp.route('/')
def index():
    if 'role' not in session:
        redirect(url_for('auth.login'))
    # TODO 开发教师接口
    elif session['role'] == MENTOR:
        pass
    elif session['role'] == STUDENT:
        pass
    elif session['role'] == ADMIN:
        pass
    else:
        abort(404)
