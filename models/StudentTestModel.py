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


    #TODO 待实现
    @classmethod
    def get_st_by_tno(cls, tno):
        """
        给出test表的id, 返回该考试的所有学生号、学生名、学生成绩

        返回数据的格式为list[dict], 每个dict有三个字段'sno'(str), 'sname'(str), 'stgrade'(int)
        例如, [{'sno': '1', 'sname': '王子轩', 'stgrade': 90}, {...}, {...}]

        :param tno: test_no考试号
        :return: list[dict](无数据则返回空list)
        """
