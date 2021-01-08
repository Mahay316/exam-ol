from datetime import datetime

from flask import session

from common.Role import *


def save_session(role, user, remember_me: str):
    """
    用户登录后存储session
    :param role: str类型，需要和Config中的定义一致
    :param user: User类型
    """
    session.clear()

    session.permanent = True if remember_me == 'true' else False
    if role == STUDENT:
        session['role'] = role
        session['no'] = user.Sno
        session['name'] = user.Sname
        session['gender'] = user.Sgender
        session['major'] = user.Smajor
    elif role == MENTOR:
        session['role'] = role
        session['no'] = user.Mno
        session['name'] = user.Mname
        session['gender'] = user.Mgender
        session['title'] = user.Mtitle
    elif role == ADMIN:
        session['role'] = role
        session['no'] = user.Ano


def if_test_end(tend, st_grade):
    """
    判断考试是否结束

    :param tend: None or timestamp
    :param st_grade: None or int
    :return: True if test ends else False
    """
    flag = False
    need_grading = False
    if tend > 0:
        # 如果考试限时，需要判断时间是不是截止了
        now = datetime.now().timestamp()
        if now > tend:
            if st_grade is None:
                # 考试结束但还没登记成绩
                # 主动判卷，判卷后重新请求考试结果
                need_grading = True
            flag = True
        else:
            if st_grade is not None:
                # 考试未结束但已经交卷
                flag = True
            else:
                # 考试未结束且未交卷
                flag = False
    else:
        if st_grade is not None:
            flag = True
    return {'over': flag, 'need_grading': need_grading}
