from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from utils import commons

from models.database import Base
metadata = Base.metadata


class Question(Base):
    __tablename__ = 'question'

    Qno = Column(String(20), primary_key=True, comment='题库中的编号')
    Qtype = Column(TINYINT(1), nullable=False, comment='题目类型')
    Qstem = Column(String(255), nullable=False, comment='题目的内容')
    Qanswer = Column(String(255), nullable=False, comment='题目的正确答案，由字典转化的字符串')
    Qselect = Column(TINYINT(1), comment='选择题的正确选项')
    Subno = Column(ForeignKey('subject.Subno', ondelete='SET NULL', onupdate='CASCADE'), index=True,
                   comment='题目所属的科目')
    Qreference = Column(INTEGER, nullable=False, server_default=text("'0'"), comment='题目被引用的次数')
    Qisdeleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='真：隐藏 假：显示')

    # subject = relationship('Subject')

    @classmethod
    def is_fill_in_blanks(cls, Qno: str):
        """
        本题是否为填空题

        :return: True if 是填空题 else False
        """
        engine = commons.get_mysql_engine()
        session = commons.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Qno == Qno)

            questions = session.query(cls).filter(*filter_list)
            if not questions.first():
                raise Exception('无该条记录')

            return questions.first().Qtype

        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def get_questions(cls, Qnos: list):

        engine = commons.get_mysql_engine()
        session = commons.get_mysql_session(engine)

        try:
            questions = []
            for Qno in Qnos:
                filter_list = []
                filter_list.append(cls.Qno == Qno)

                question = session.query(cls).filter(*filter_list)
                if not questions.first():
                    raise Exception("无该条记录")
                questions.append(question.first())

            return questions

        except Exception as e:
            session.rollback()
            raise e
