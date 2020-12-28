#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/27 11:15
# @Author  : kiwanter
# @Email   : kiwanter@163.com
# @File    : StudentCourseModel.py
# @software: pycharm

'''
@file function:
'''

from sqlalchemy import Column, ForeignKey

from models.database import Base


class StudentCourse(Base):
    __tablename__ = 'student_course'

    Cno = Column(ForeignKey('course.Cno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, comment='课程编号')
    Sno = Column(ForeignKey('student.Sno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True, comment='学生编号')
