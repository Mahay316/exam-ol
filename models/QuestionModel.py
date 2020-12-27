from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, ENUM
from common import model_common

from models.database import Base
from common import model_common
from models.SubjectModel import Subject


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

        try:
            if self.Qtype == 'fill':
                return True
            else:
                return False

        except Exception as e:
            raise e

    @classmethod
    def get_questions(cls, Qnos: list):

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

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


    # TODO 待实现
    @classmethod
    def select_questions_by(cls, subject=None, qtype=None, qno=None, content=None):
        """
        通过筛选条件筛出所需试题，只有一个参数不为None

        :param subject: 科目筛选字符串，直接全字匹配
        :param qtype: 类型筛选，'select', 'multi', 'fill'三种其一
        :param qno: 按题号直接搜索
        :param content: 按内容搜索模糊匹配
        :return: list[Question](无内容则返回空list)
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []

            if subject:
                subno = Subject.get_subnos_by_subname(subject)
                filter_list.append(cls.Subno == subno)

            elif qtype:
                filter_list.append(cls.Qtype == qtype)

            elif qno:
                filter_list.append(cls.Qno == qno)

            elif content:
                filter_list.append(cls.Qstem.like('%'+content+'%'))

            else:
                return []

            return session.query(cls).filter(*filter_list).all()


        except Exception as e:
            raise e
