#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/27 13:36
# @Author  : kiwanter
# @Email   : kiwanter@163.com
# @File    : SubjectModel.py
# @software: pycharm

'''
@file function:
'''
from sqlalchemy import Column, VARCHAR, Integer, String

from models.database import Base
from common import model_common


class Subject(Base):
    __tablename__ = 'subject'

    Subno = Column(Integer, primary_key=True, comment='科目编号')
    Subname = Column(String(25, 'utf8mb4_general_ci'), nullable=False, index=True, comment='科目名称')

    @classmethod
    def get_subno_by_subname(cls, subname):

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Subname == subname)

            sub = session.query(cls).filter(*filter_list).first()
            if sub:
                return sub.Subno
            else:
                raise Exception('没有该名称的学科信息')

        except Exception as e:
            return e

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def get_all_subs(cls):
        """
        获取全部科目对象

        :return: list[Subject]
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            return session.query(cls).all()

        except Exception as e:
            session.rollback()
            raise e

        finally:
            engine.dispose()
            session.remove()
