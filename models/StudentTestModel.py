#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 15:58
# @Author  : kiwanter
# @Email   : kiwanter@163.com
# @File    : StudentTestModel.py
# @software: pycharm

'''
@file function:
'''

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Table, text
from sqlalchemy.dialects.mysql import ENUM, INTEGER, TINYINT, VARCHAR
from sqlalchemy.orm import relationship

from models.database import Base
from models.TestModel import Test


class StudentTest(Base):
    __tablename__ = 'student_test'

    Tno = Column(ForeignKey('test.Tno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False,
                 comment='考试编号')
    Sno = Column(ForeignKey('student.Sno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False,
                 index=True, comment='学生编号')
    STgrade = Column(Integer, comment='学生考试成绩')

    # student = relationship('Student')
    test = relationship('Test')
