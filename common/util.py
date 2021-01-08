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

