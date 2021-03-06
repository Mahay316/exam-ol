from sqlalchemy import Column, ForeignKey, TIMESTAMP, Integer, String
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from common import model_common
from models.PaperModel import Paper
from models.QuestionModel import Question
from datetime import datetime

from models.database import Base
from models.QuestionPaperModel import QuestionPaper


class Test(Base):
    __tablename__ = 'test'

    Tno = Column(Integer, primary_key=True, comment='考试的编号')
    Tname = Column(String(20, 'utf8mb4_general_ci'), nullable=False, comment='考试的名称')
    Tdesc = Column(String(255, 'utf8mb4_general_ci'), comment='考试说明')
    Tstart = Column(TIMESTAMP, nullable=False, default=datetime.utcnow(), comment='考试开始时间')
    Tend = Column(TIMESTAMP, comment='考试结束时间')
    Pno = Column(ForeignKey('paper.Pno', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True,
                 comment='引用的试卷编号')
    Cno = Column(ForeignKey('course.Cno', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True,
                 comment='所属的课程编号')

    # course = relationship('Course')
    paper = relationship('Paper')

    @classmethod
    def get_test(cls, Tno):
        """
        根据考试号返回Test(考试)对象

        :param Tno:
        :return: 返回Test对象，如果考试不存在则返回None
        """
        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Tno == Tno)

            tests = session.query(cls).filter(*filter_list)
            if not tests.first():
                return None

            return tests.first()

        except Exception as e:
            session.rollback()
            raise e

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def get_all_question_id(cls, Tno) -> list:
        """
        根目据考试号返回考试的全部题id

        :param Tno:
        :return: 所有id做成一个list返回，每个id均为str类型
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Tno == Tno)

            tests = session.query(cls).filter(*filter_list)
            if not tests.first():
                return None

            return Paper.get_questions_id(tests.first().Pno)

        except Exception as e:
            session.rollback()
            raise e

        finally:
            engine.dispose()
            session.remove()

    def get_begin_time(self):
        """
        获得考试开始时间，类型是datetime
        """

        return self.Tstart

    def get_end_time(self):
        """
        获取考试结束时间

        :return: 类型是datetime, 如果考试不限时间则返回None
        """

        return self.Tend

    # 改为list[(Question, qpscore)]，即每个元素是tuple，0号元素是Question对象，1号元素是在本卷中的分值
    def get_all_questions(self) -> list:
        """
        获取本考试的所有试题

        :return: 返回list[(Question, qpscore)]
        """
        Qnos = Paper.get_questions_id(self.Pno)
        Questions = Question.get_questions(Qnos)

        l = []

        for q in Questions:
            try:
                l.append((q, QuestionPaper.get_qpscore(pno=self.Pno, qno=q.Qno)))
            except:
                continue

        return l

    @classmethod
    def get_paper_by_tno(cls, tno) -> Paper:
        """
        通过test_no获取Paper对象

        :return: Paper or None
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Tno == tno)

            t = session.query(cls).filter(*filter_list).first()
            if not t:
                raise Exception('没有该试卷号记录')

            return Paper.get_paper(t.Pno)

        except Exception as e:
            session.rollback()
            raise e

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def set_test_grade(cls, tno, sno, st_wrong, st_blank, st_grade):
        """
        设置本次考试的学生成绩

        :param tno: test_no
        :param sno: student_no
        :param st_wrong: 错误题数
        :param st_blank: 空题数
        :param st_grade: 考试成绩
        """

        from models.StudentTestModel import StudentTest
        return StudentTest.add_st(tno=tno, sno=sno, stwrong=st_wrong, stblank=st_blank, stgrade=st_grade)

    @classmethod
    def get_test_infos(cls, tno) -> dict:
        """
        教师端获取班级考试统计信息

        :return: dict or None
        {'grades': [int], 'pscore': int}
        grades: 是所有参加tno的学生的考试成绩(无需学生信息)
        pscore: 卷子总分
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Tno == tno)

            test = session.query(cls).filter(*filter_list).first()
            if not test:
                raise Exception('没有该考试号记录')

            from models.StudentTestModel import StudentTest
            grades = StudentTest.get_all_grades(tno=tno)

            pscore = test.paper.Pscore

            return {
                'grades': grades,
                'pscore': pscore
            }

        except Exception as e:
            session.rollback()
            raise e

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def get_student_test_info(cls, tno, sno) -> dict:
        """
        获取某个学生的某次考试的信息
        这里理应用视图，因为涉及两个对象的信息，此处为简便使用了字典，有时间可以优化

        :return: dict or None{
            'st_grade': int, 学生成绩
            'pscore': int, 卷子总分
            'st_wrong': int, 错误题数
            'pnum': int, 卷子题目总数
            'st_blank': int, 未作答题目数
            'tstart': 时间戳
            'tend': 时间戳
            'tname': 考试名称
            'tdesc':
        }
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Tno == tno)

            test = session.query(cls).filter(*filter_list).first()
            paper = test.paper

            from models.StudentTestModel import StudentTest
            st = StudentTest.get_st(tno=tno, sno=sno)

            test_dict = {
                'st_grade': st.STgrade,
                'pscore': paper.Pscore,
                'st_wrong': st.STwrong,
                'pnum': paper.Pnum,
                'st_blank': st.STblank,
                'tstart': test.Tstart.timestamp(),
                'tname': test.Tname,
                'tdesc': test.Tdesc,
                'tend': -1 if test.Tend is None else test.Tend.timestamp()
            }

            return test_dict

        except Exception as e:
            session.rollback()
            raise e

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def add_test(cls, pno, cno, tname, tdesc, tstart, tend):
        """
        发布考试
        同时将更新StudentTest
        :param tname:
        :param tstart: 时间戳
        :param tend: 时间戳
        :return True if succeed else False
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            from models.CourseModel import Course
            snos = [s.Sno for s in Course.get_students_by_no(cno)]

            test = Test(
                Tname=tname,
                Tdesc=tdesc,
                Pno=pno,
                Cno=cno
            )

            if tstart:
                test.Tstart=model_common.change_stamp_to_datatime(int(tstart))
            if tend:
                test.Tend = model_common.change_stamp_to_datatime(int(tend))

            session.add(test)
            session.commit()

            from models.StudentTestModel import StudentTest
            StudentTest.add_snos_and_tno(tno=test.Tno, snos=snos)

            return True

        except Exception as e:
            session.rollback()
            raise e
            return False

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def delete_test(cls, tno):
        """
        调用存储过程删除考试
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Tno == tno)

            test = session.query(cls).filter(*filter_list).first()
            if not test:
                raise Exception('没有该考试记录')

            session.delete(test)
            session.commit()

            return True

        except Exception as e:
            session.rollback()
            return False

        finally:
            engine.dispose()
            session.remove()
