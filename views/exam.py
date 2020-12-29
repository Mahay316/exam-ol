from flask import Blueprint, request, jsonify, session
from models import Test
from datetime import datetime
import json
from models import Student, Paper
from decorators import should_be
from common.Role import *

exam_bp = Blueprint('exam_bp', __name__)


@should_be([STUDENT])
def permission_inadequate_or_exam_not_exists(test: Test):
    """
    检查访问是否合法

    :param test: 考试对象
    :return: 若不合法则返回需要的json，合法则返回None
    """
    res = {}
    if test is None:
        # 考试不存在
        res['code'] = 403
        res['msg'] = '考试不存在'
        return jsonify(res)

    if 'test_ids' not in session:
        # 缓存学生所有考试，判断是否含有本次考试(避免每次都从数据库查找)
        session['test_ids'] = Student.get_user(session['no']).get_all_test_ids()

    if session['test_ids'] is None or test.Tno not in session['test_ids']:
        # 无权访问
        res['code'] = 403
        res['msg'] = '无权访问'
        return jsonify(res)
    return None


def guarantee_exam_begin(test: Test):
    """
    确保考试开始

    :param test: 考试对象
    :return: 考试未开始则返回需要返回的错误信息，正常则返回None
    """
    res = {}
    cur_time = datetime.now()
    begin_time = test.get_begin_time()
    if cur_time < begin_time:
        res['code'] = 204
        res['msg'] = '考试未开始'
        return jsonify(res)

    return None


@exam_bp.route('/time', methods=['GET'])
@should_be([STUDENT])
def get_exam_time_info():
    """
    获得考试时间信息
    """
    examID = request.form.get('examID')
    test = Test.get_test(examID)

    # 检查访问合法性
    validated = permission_inadequate_or_exam_not_exists(test)
    if validated is not None:
        return validated

    # res为待返回数据
    res = {}
    cur_time = datetime.now()
    elapsed_time = test.get_begin_time()
    time_passed = 0

    if cur_time >= elapsed_time:
        time_passed = (cur_time - elapsed_time).total_seconds()
    res['elapsedTime'] = int(time_passed)

    end_time = test.get_end_time()
    res['timeLeft'] = -time_passed
    res['hasLimit'] = False
    if end_time is not None:
        res['timeLeft'] = int((end_time - cur_time).total_seconds())
        res['hasLimit'] = True

    res['code'] = 200
    return jsonify(res)


@exam_bp.route('/questions', methods=['GET'])
@should_be([STUDENT])
def get_questions():
    """
    请求题目内容

    :return: json格式数据
    """
    examID = request.args['examID']

    test = Test.get_test(examID)
    validated = permission_inadequate_or_exam_not_exists(test)
    if validated is not None:
        return validated

    validated = guarantee_exam_begin(test)
    if validated is not None:
        return validated

    res_dict = {
        'code': 200,
        'questions': []
    }
    res = res_dict['questions']

    if 'answer' not in session:
        session['answer'] = {}

    for tp in test.get_all_questions():
        q = tp[0]
        qpscore = tp[1]
        cur_dict = {
            'questionID': q.Qno,
            'type': q.Qtype,
            'stem': q.Qstem, # 题干字符串
            'choices': "", # 选择题的选项，填空题无
            'cache': "",
            'qpscore': qpscore
        }

        # 为了后面判卷不用再次访问数据库，暂时缓存下来
        # TODO 未测试
        session['answers'][q.Qno] = {
            'qanswer':json.loads(q.Qanswer),
            'qtype': q.Qtype,
            'qpscore': qpscore
        }

        # 如果是选择题则choices置空
        if not q.is_fill_in_blanks():
            cur_dict['choices'] = json.dumps(q.Qselect)

        # 用户已作答的缓存
        if q.Qno in session:
            tmp = {
                'questionID': q.Qno,
                'choice': session[q.Qno]['choice'],
                'submitTime': session[q.Qno]['submitTime']
            }
            cur_dict['cache'] = tmp

        res.append(cur_dict)

    # res是个list，其每个元素为dict，格式如下
    # cur_dict = {
    #     'questionID': "1234",
    #     'code': 200,
    #     'type': "select",
    #     'stem': "question stem",
    #     'choices': json.dumps({"A": 1, "B": 2, "C": 3}),
    #     'cache': {'choice': ['A', 'B'], 'submitTime': '1607591913'}
    # }

    return jsonify(res_dict)


@exam_bp.route('/questions', methods=['POST'])
@should_be([STUDENT])
def cache_questions():
    """
    缓存考生作答情况
    """
    examID = request.form['examID']

    test = Test.get_test(examID)
    # 确保权限满足且考试存在
    validated = permission_inadequate_or_exam_not_exists(test)
    if validated is not None:
        return validated

    # 确保考试已开始（正常使用web前端不会出现该情况）
    validated = guarantee_exam_begin(test)
    if validated is not None:
        return validated

    # session缓存已保存的题目id
    if 'cached_questionID' not in session:
        # 由于session需要序列化因此不能用set(), 在这里用list然后返回时用set去重
        session['cached_questionID'] = list()

    # 获得的result是个list，元素为dict
    result = json.loads(request.form['result'])
    assert isinstance(result, list)

    # 将内容缓存
    for per_res in result:
        assert isinstance(per_res, dict)
        # TODO 未判断题目是否存在
        questionID = per_res.pop('questionID')
        # cached_questionID.add(questionID)
        session[questionID] = per_res
        session['cached_questionID'].append(questionID)

    # session缓存所有题目id
    if 'all_question_id' not in session:
        session['all_question_id'] = Test.get_all_question_id(examID)

    res = {
        'code': 200,
        'cached': list(set(session['cached_questionID'])),
        'all': list(session['all_question_id'])
    }

    return jsonify(res)


@exam_bp.route('/grading', methods=['POST'])
@should_be([STUDENT])
def grade_exam():
    """
    试卷判分接口，直接使用后端缓存的数据
    """
    tno = int(request.form['tno'])
    # TODO 进行权限验证，即验证学生是否有该考试且考试已经开始
    paper = Test.get_paper_by_tno(tno)
    if paper is None:
        return jsonify({'code': 204})
    pnum = paper.Pnum
    right_num, did_num, stu_grade = 0, 0, 0

    for quiz_id in list(set(session['cached_questionID'])):
        did_num += 1
        answer = session['answers'][quiz_id]
        qtype = answer['qtype']
        # ["A", "B"]
        qanswer = answer['qanswer']
        qpscore = answer['qpscore']

        # {'choice': ["A", "B"]}
        user_ans = session[quiz_id]['choice']
        flag = False
        if qtype == 'select':
            flag = qanswer[0] == user_ans[0]
        elif qtype == 'multi':
            user_ans.sort()
            qanswer.sort()
            flag = user_ans == qanswer
        elif qtype == 'fill':
            flag = user_ans == qanswer
        if flag:
            right_num += 1
            stu_grade += qpscore

    Test.set_test_grade(tno, session['no'], st_wrong=pnum - right_num, st_blank=pnum - did_num, st_grade=stu_grade)

    # TODO 未清理session

    return jsonify({'code': 200})

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
#     判卷，判卷完成后清楚服务端的作答缓存
#     """