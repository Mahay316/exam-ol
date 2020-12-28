#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/15 19:10
# @Author  : kiwanter
# @Email   : kiwanter@163.com
# @File    : QuestionPaperModel.py
# @software: pycharm

'''
@file function:
'''

from sqlalchemy import Column, ForeignKey, Integer, text
from sqlalchemy.orm import relationship

from models.database import Base
# from models.PaperModel import Paper
# from models.QuestionModel import Question

from common import model_common

class QuestionPaper(Base):
    __tablename__ = 'question_paper'

    Pno = Column(ForeignKey('paper.Pno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False,
                 comment='题库中的编号')
    Qno = Column(ForeignKey('question.Qno', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False,
                 index=True, comment='试卷的编号')
    QPscore = Column(Integer, server_default=text("'0'"), comment='试题的分值ֵ')
    QPposition = Column(Integer, comment='题目在试卷中的位置')

    # paper = relationship('Paper')
    # question = relationship('Question')

    @classmethod
    def add_question_to_paper(cls, pno, qno, score, position):
        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            qp = QuestionPaper(
                Pno=pno,
                Qno=qno,
                QPscore=score,
                QPposition=position
            )
            session.add(qp)
            session.commit()
            return True

        except Exception as e:
            session.rollback()
            return False

        finally:
            engine.dispose()
            session.remove()