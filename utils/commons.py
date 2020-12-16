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