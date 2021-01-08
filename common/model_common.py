#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/14 22:18
# @Author  : kiwanter
# @Email   : kiwanter@163.com
# @File    : commons.py
# @software: pycharm

"""
@file function:
"""
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import config


def get_mysql_engine():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI,
                           pool_size=config.POOL_SIZE,
                           max_overflow=config.MAX_OVERFLOW,
                           pool_recycle=7200
                           )
    return engine


def get_mysql_session(engine):
    Session = scoped_session(sessionmaker(bind=engine))
    return Session


def get_page_by_list(list: list, page=1):
    pagesize = config.PAGE_SIZE
    length = len(list)

    if page <= 0:
        return []
    elif (page - 1) * pagesize > length:
        return []
    elif page * pagesize > length:
        return list[((page - 1) * pagesize):]
    else:
        return list[((page - 1) * pagesize):(page * pagesize)]


def change_stamp_to_datatime(timeStamp):
    dateArray = datetime.utcfromtimestamp(timeStamp)
    return dateArray.strftime("%Y--%m--%d %H:%M:%S")


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
