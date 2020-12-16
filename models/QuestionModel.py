from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, ENUM
from common import commons

from models.database import Base
metadata = Base.metadata


class Question(Base):
    __tablename__ = 'question'

    Qno = Column(String(20, 'utf8mb4_general_ci'), primary_key=True, comment='题库中的编号')
    Qtype = Column(ENUM('select', 'multi', 'fill'), nullable=False, comment='题目类型 select-单选 multi-多选 fill-填空')
    Qstem = Column(String(255, 'utf8mb4_general_ci'), nullable=False, comment='题目的内容')
    Qanswer = Column(String(255, 'utf8mb4_general_ci'), nullable=False, comment='JSON格式的题目的答案，选择题的备选项，填空题的答案')
    Qselect = Column(String(10, 'utf8mb4_general_ci'), comment='选择题的正确选项')
    Subno = Column(ForeignKey('subject.Subno', ondelete='SET NULL', onupdate='CASCADE'), index=True,
                   comment='题目所属的科目')
    Qreference = Column(INTEGER, nullable=False, server_default=text("'0'"), comment='题目被引用的次数')
    Qisdeleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='真：隐藏 假：显示')

    # subject = relationship('Subject')

    def is_fill_in_blanks(self):
        """
        本题是否为填空题

        :return: True if 是填空题 else False
        """
        engine = commons.get_mysql_engine()
        session = commons.get_mysql_session(engine)

        try:
            if self.Qtype == 'fill':
                return True
            else:
                return False

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
                if not question.first():
                    raise Exception("无该条记录")
                questions.append(question.first())

            return questions

        except Exception as e:
            session.rollback()
            raise e
