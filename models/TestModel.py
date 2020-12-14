from sqlalchemy import CHAR, Column, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from utils import commons

Base = declarative_base()
metadata = Base.metadata

class Test(Base):
    __tablename__ = 'test'

    Tno = Column(CHAR(20), primary_key=True, comment='考试的编号')
    Tname = Column(VARCHAR(20), nullable=False, comment='考试的名称')
    Tstart = Column(TIMESTAMP, nullable=False, comment='考试开始时间')
    Tend = Column(TIMESTAMP, comment='考试结束时间')
    Pno = Column(ForeignKey('paper.Pno', ondelete='RESTRICT', onupdate='CASCADE'), index=True, comment='引用的试卷编号')
    Cno = Column(ForeignKey('class.Cno', ondelete='RESTRICT', onupdate='CASCADE'), index=True, comment='所属的课程编号')

    # course = relationship('Course')
    # paper = relationship('Paper')

    @staticmethod
    @classmethod
    def get_test(cls, Tno: str):
        """
        根据考试号返回Test(考试)对象

        :param Tno:
        :return: 返回Test对象，如果考试不存在则返回None
        """
        engine = commons.get_mysql_engine()
        session = commons.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Tno == Tno)

            questions = session.query(cls).filter(*filter_list)
            if not questions.first():
                return None

            return questions.first()

        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    @classmethod
    def get_all_question_id(cls, Tno: str) -> list:
        """
        根据考试号返回考试的全部题目id

        :param Tno:
        :return: 所有id做成一个list返回，每个id均为str类型
        """
        
    def get_begin_time(self):
        """
        获得考试开始时间，类型是datetime
        """

    def get_end_time(self):
        """
        获取考试结束时间

        :return: 类型是datetime, 如果考试不限时间则返回None
        """

    def get_all_questions(self) -> list:
        """
        获取本考试的所有试题

        :return: 返回list[Question]
        """
