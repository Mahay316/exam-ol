#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/15 13:25
# @Author  : kiwanter
# @Email   : kiwanter@163.com
# @File    : PaperModel.py
# @software: pycharm

"""
@file function:
"""
from sqlalchemy import Column, ForeignKey, Integer, String, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

from models.database import Base
from common import commons

metadata = Base.metadata


class Paper(Base):
    __tablename__ = 'paper'

    Pno = Column(String(20, 'utf8mb4_general_ci'), primary_key=True, comment='试卷的编号')
    Pname = Column(String(30, 'utf8mb4_general_ci'), comment='试卷名')
    Subno = Column(ForeignKey('subject.Subno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='科目编号')
    Preference = Column(Integer, server_default=text("'0'"), comment='试卷被引用的次数')
    Pisdeleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='真：隐藏 假：显示')

    # subject = relationship('Subject')
    questionpaper = relationship('QuestionPaper', backref='paper')

    @classmethod
    def get_questions_id(cls, Pno: str) -> list:
        '''
            返回试卷的全部试题号
        :param Pno:
        :return:【Qno】
        '''
        engine = commons.get_mysql_engine()
        session = commons.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Pno == Pno)

            questionpapers = session.query(cls).filter(*filter_list).first().questionpaper

            qnos = []
            for x in questionpapers:
                qnos.append(x.Qno)
            return qnos


        except Exception as e:
            raise e

