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

from common import model_common
from models.database import Base


class Paper(Base):
    __tablename__ = 'paper'

    Pno = Column(Integer, primary_key=True, comment='试卷的编号')
    Pname = Column(String(30, 'utf8mb4_general_ci'), index=True, comment='试卷名')
    Subno = Column(ForeignKey('subject.Subno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='科目编号')
    Pnum = Column(Integer, nullable=False, comment='试卷包含的题目数量')
    Pscore = Column(Integer, nullable=False, comment='试卷总分')
    Preference = Column(Integer, server_default=text("'0'"), comment='试卷被引用的次数')
    Pisdeleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='真：隐藏 假：显示')

    # subject = relationship('Subject')
    questionpaper = relationship('QuestionPaper', backref='paper')

    @classmethod
    def get_questions_id(cls, Pno) -> list:
        '''
            返回试卷的全部试题号
        :param Pno:
        :return:【Qno】
        '''
        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Pno == Pno)

            questionpapers = session.query(cls).filter(*filter_list).first().questionpaper

            qnos = []
            for x in questionpapers:
                qnos.append(x.Qno)
            return qnos

        except Exception as e:
            session.rollback()
            raise e

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def get_all_papers(cls):
        """
        获取全部试卷

        :return: list[Paper](没有则返回空list)
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []

            return session.query(cls).filter(*filter_list).all()

        except Exception as e:
            session.rollback()
            raise e

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def select_papers_by(cls, page=1, subject=None, used=None, pno=None, pname=None):

        """
        模式和Question里的select_questions_by很类似
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Pisdeleted == 0)

            if subject:
                filter_list.append(cls.Subno == subject)

            if used == False:
                filter_list.append(cls.Preference == 0)

            elif used == True:
                filter_list.append(cls.Preference != 0)

            if pno:
                filter_list.append(cls.Pno == pno)

            if pname:
                filter_list.append(cls.Pname.like('%' + pname + '%'))

            papers = session.query(cls).filter(*filter_list)
            res = (papers.count(), model_common.get_page_by_list(papers.all(), page))
            return res

        except Exception as e:
            session.rollback()
            raise e

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def add_paper(cls, questions, pname, subno):
        """
        组卷
        接口计算pscore和pnum

        :param questions: [{'qno': '001', 'qpscore': 3}, {...}, {...}]
        :param pname: 试卷名
        :param subno: 试卷科目
        :return: 成功返回True，失败False
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            pscore = 0
            for q in questions:
                pscore += q['qpscore']

            paper = Paper(Pname=pname,
                          Subno=subno,
                          Pnum=len(questions),
                          Pscore=pscore)

            session.add(paper)
            session.commit()

            from models import QuestionPaper
            QuestionPaper.add_questions_to_paper(pno=paper.Pno, questions=questions)

            return True

        except Exception as e:
            session.rollback()
            return False

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def delete_paper(cls, pno):
        """
        删除试卷
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Pno == pno)

            question = session.query(cls).filter(*filter_list)
            if not question.first():
                raise Exception('没有该试卷号记录')

            question.update({'Pisdeleted': 1})
            session.commit()
            return True

        except Exception as e:
            session.rollback()
            return False

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def get_paper_num(cls) -> int:
        """
        获取所有试卷数量
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Pisdeleted == 0)

            return session.query(cls).filter(*filter_list).count()

        except Exception as e:
            session.rollback()
            raise e

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def get_paper(cls, pno):
        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Pno == pno)

            return session.query(cls).filter(*filter_list).first()

        except Exception as e:
            session.rollback()
            raise e

        finally:
            engine.dispose()
            session.remove()
