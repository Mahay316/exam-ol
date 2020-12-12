from flask import Blueprint, request, jsonify
from flask_login import current_user
from models import Test
from datetime import datetime

exam_bp = Blueprint('exam_bp', __name__)


@exam_bp.route('/time', methods=['GET'])
def get_exam_time_info():
    """
    获得考试时间信息
    """
    examID = request.form.get('examID')
    test = Test.get_test(examID)
    res = {}
    if test is None:
        # 考试不存在
        res['code'] = 403
        res['msg'] = '考试不存在'
        return jsonify(res)

    if not (current_user.is_student() and current_user.has_this_exam(test)):
        # 无权访问
        res['code'] = 403
        res['msg'] = '无权访问'
        return jsonify(res)

    cur_time = datetime.now()
    elapsed_time = test.get_begin_time()
    time_passed = 0

    if cur_time >= elapsed_time:
        time_passed = (cur_time - elapsed_time).timestamp()
    res['elapsedTime'] = int(time_passed)

    end_time = test.get_end_time()
    res['timeLeft'] = -time_passed
    res['hasLimit'] = False
    if end_time is not None:
        res['timeLeft'] = int((end_time - cur_time).timestamp()  )
        res['hasLimit'] = True

    res['code'] = 200
    return jsonify(res)


@exam_bp.route('/questions', methods=['GET', 'POST'])
def questions():
    # 请求题目内容或者缓存考生作答情况
    if request.method == 'GET':
        # TODO 获取题目内容
        pass
    elif request.method == 'POST':
        # TODO 缓存考生刚刚修改的题目的答案
        pass

# TODO 判卷请求似乎没有

# @exam_bp.route("/<str:exam_id>", method=['GET'])
# def get_paper(exam_id: str):
#     """
#     点击试卷链接后给前端返回试卷
#     """
#     pass
#
#
# def check_paper():
#     """
#     判卷
#     """
