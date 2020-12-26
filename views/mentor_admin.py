from flask import Blueprint, request, jsonify, session, redirect, url_for, abort, render_template
from models import Test
from datetime import datetime
from common.Role import *
from decorators import should_be
import json

mentor_bp = Blueprint('mentor_bp', __name__)


@mentor_bp.route('/class')
@should_be([MENTOR])
def teacher_admin():
    """
    展示全部班级

    :return 全部班级信息的json
    """


@mentor_bp.route('/class/<string:class_id>', methods=['GET', 'POST'])
@should_be([MENTOR])
def class_management(class_id: str):
    """
    班级信息管理
    GET方法获取学生信息和考试列表，POST方法给出考试id，返回考试统计结果
    """


@mentor_bp.route('/paper')
@should_be([MENTOR])
def paper_management():
    """
    试卷管理页面
    """


@mentor_bp.route('/questions')
@should_be([MENTOR])
def question_management():
    """
    题目管理
    """
