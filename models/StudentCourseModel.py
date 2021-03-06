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
from common import model_common


class StudentCourse(Base):
    __tablename__ = 'student_course'

    Cno = Column(ForeignKey('course.Cno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False,
                 comment='课程编号')
    Sno = Column(ForeignKey('student.Sno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False,
                 index=True, comment='学生编号')

    @classmethod
    def add_class_member(cls, cno, sno):
        """
        为班级增加学生

        :param cno: 课程号
        :param sno: 学生学号
        :return: 成功返回True， 学生已存在返回False
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            sc = StudentCourse(Cno=cno,
                               Sno=sno)
            session.add(sc)
            session.commit()
            return True

        except Exception as e:
            session.rollback()
            return False

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def del_class_member(cls, cno, sno):
        """
        为班级删除学生

        :param cno: 课程号
        :param sno: 学生学号
        :return: 成功返回True，学生不存在返回False
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Cno == cno)
            filter_list.append(cls.Sno == sno)

            sc = session.query(cls).filter(*filter_list).first()

            session.delete(sc)
            session.commit()
            return True

        except Exception as e:
            session.rollback()
            return False

        finally:
            engine.dispose()
            session.remove()
