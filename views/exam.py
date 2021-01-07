from flask import Blueprint, request, jsonify, session, current_app
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
    examID = int(request.args.get('examID'))
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
        time_passed = int((cur_time - elapsed_time).total_seconds())
    res['elapsedTime'] = int(time_passed)

    end_time = test.get_end_time()
    res['timeLeft'] = -time_passed
    res['hasLimit'] = False
    if end_time is not None:
        res['timeLeft'] = int((end_time - cur_time).total_seconds())
        res['hasLimit'] = True

    res['code'] = 200
    res['tname'] = test.Tname
    return jsonify(res)


@exam_bp.route('/questions', methods=['GET'])
@should_be([STUDENT])
def get_questions():
    """
    请求题目内容

    :return: json格式数据
    """
    examID = int(request.args['examID'])

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

    if 'answers' not in session:
        session['answers'] = {}

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
            cur_dict['choices'] = json.loads(q.Qselect)

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
    examID = int(request.form.get('examID'))

    test = Test.get_test(examID)
    # TODO 增加是否判卷的判断，如果考试结束直接判卷
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
    print(result)
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
    if 'all_question_ids' not in session:
        session['all_question_ids'] = Test.get_all_question_id(examID)

    res = {
        'code': 200,
        'cached': list(set(session['cached_questionID'])),
        'all': list(session['all_question_ids'])
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

    # TODO 判断考试是否结束

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

    # TODO 清理session易出错, session存储逻辑要改变，为了
    for quiz_id in list(set(session['cached_questionID'])):
        del session[quiz_id]
    del session['cached_questionID']
    del session['all_question_ids']
    del session['answers']

    return jsonify({'code': 200})

@exam_bp.route('/', methods=['GET'])
@should_be([MENTOR, STUDENT])
def get_exam_results():
    """
    根据身份获取考试成绩信息
    教师返回班内所有同学统计信息，学生返回本次考试成绩
    """
    role = session['role']
    if role == MENTOR:
        # TODO 验证老师是否有考试
        tno = int(request.args['tno'])

        infos = Test.get_test_infos(tno)

        if infos is None:
            return jsonify({'code': 204})

        res_json = {
            'code': 200,
            'pscore': infos['pscore']
        }

        stat_dict = {}
        # 分10段，左闭右开，增序成绩
        # 为处理右边界多开stat_dict[10]元素
        for i in range(11):
            stat_dict[i] = 0

        for grade in infos['grades']:
            stat_dict[grade // 10] += 1

        stat_dict[9] += stat_dict[10]

        segments = []
        for i in range(10):
            segments.append(stat_dict[i])

        res_json['segments'] = segments
        return jsonify(res_json)
    else:
        # TODO 验证学生是否有考试
        tno = int(request.args['tno'])

        # TODO 增加判断考试是否完成的接口（已完成考试分两种情况时间截止(考了和没考)和提交卷子但时间没截止）
        # TODO 要先判断考试是否结束
        # TODO 根据作答情况要是结束了没作答

        # TODO 请求考试成绩的时候结束了的话要判个卷，主动调一下判卷接口
        infos = Test.get_student_test_info(tno, session['no'])

        if infos is None:
            return jsonify({'code': 403})

        tend = infos.get('tend')
        st_grade = infos.get('st_grade')
        infos['over'] = False
        if tend is not None:
            # 如果考试限时，需要判断时间是不是截止了
            now = datetime.now().timestamp()
            if now > tend:
                infos['over'] = True
                if st_grade is None:
                    # 考试结束但还没登记成绩
                    # TODO 主动判卷，判卷完成后返回考试信息
                    pass
            else:
                if st_grade is not None:
                    # 考试未结束但已经交卷
                    infos['over'] = True
                else:
                    # 考试未结束且未交卷
                    infos['over'] = False

        infos['code'] = 200
        return jsonify(infos)


@exam_bp.route('/', methods=['POST'])
@should_be([MENTOR])
def add_exam():
    """
    发布考试
    """
    form = request.form
    pno = int(form.get('pno'))
    cno = int(form.get('cno'))
    tname = form.get('tname')
    tdesc = form.get('tdesc')
    tstart = form.get('tstart')
    tend = form.get('tend')

    flag = Test.add_test(pno=pno, cno=cno, tname=tname, tdesc=tdesc, tstart=tstart, tend=tend)

    if not flag:
        return jsonify({'code': 204})

    return jsonify({'code': 200})


# TODO
@exam_bp.route('/', methods=['DELETE'])
@should_be([MENTOR])
def delete_exam():
    """
    删除考试
    """
    tno = request.args.get('tno')
    Test.delete_test(tno)
    return jsonify({'code': 200})


@exam_bp.route('/paper')
@should_be([STUDENT], do='404')
def get_exam_page():
    return current_app.send_static_file('html/test_online.html')


@exam_bp.route('/detail')
@should_be([STUDENT], do='404')
def get_exam_detail_page():
    return current_app.send_static_file('html/test_detail.html')
