from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from models.database import Base
from models.StudentCourseModel import StudentCourse
from models.TestModel import Test
from common import model_common


class Course(Base):
    __tablename__ = 'course'

    Cno = Column(Integer, primary_key=True, comment='课程编号')
    Cname = Column(String(20, 'utf8mb4_general_ci'), nullable=False, comment='课程名称')
    Subno = Column(ForeignKey('subject.Subno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='课程所属科目')
    Mno = Column(ForeignKey('mentor.Mno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='教授该课程教师号')

    # mentor = relationship('Mentor')
    # subject = relationship('Subject')
    # student = relationship('Student', secondary='student_course')

    tests = relationship('Test', backref='Course')
    studentcourse = relationship('StudentCourse', backref='Course')

    @classmethod
    def get_tests_by_no(cls, course_no):
        """
        根据课程号返回该课程下所拥有的全部考试对象

        :param course_no: 课程号
        :return: list[Test]
        """
        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:

            filter_list = []
            filter_list.append(cls.Cno == course_no)

            course = session.query(cls).filter(*filter_list).first()

            if not course:
                raise Exception('没有该课程号记录')
            return course.tests

        except Exception as e:
            raise e

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def get_students_by_no(cls, course_no):
        """
        根据课程号返回该课程下所拥有的全部学生对象

        :param course_no: 课程号
        :return: list[Student]
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Cno == course_no)

            students = []

            course = session.query(cls).filter(*filter_list).first()

            if not course:
                raise Exception('没有该课程号记录')

            from models.UserModel import Student
            for sc in course.studentcourse:
                students.append(Student.get_user(sc.Sno))
            return students

        except Exception as e:
            raise e

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def get_class(cls, Cno):
        """
        返回课程对象,没有则返回none

        :param Cno: 课程号
        :return: Course/None
        """

        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Cno == Cno)

            return session.query(cls).filter(*filter_list).first()

        except Exception as e:
            session.rollback()
            raise e

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def add_class_member(cls, cno, sno):
        """
        为班级增加学生

        :param cno: 课程号
        :param sno: 学生学号
        :return: 成功返回True， 学生已存在返回False
        """

        return StudentCourse.add_class_member(cno=cno, sno=sno)

    @classmethod
    def del_class_member(cls, cno, sno):
        """
        为班级删除学生

        :param cno: 课程号
        :param sno: 学生学号
        :return: 成功返回True，学生不存在返回False
        """

        return StudentCourse.del_class_member(cno=cno, sno=sno)

    @classmethod
    def get_test_info_by_cno(cls, cno):
        """
        给出cno返回该课程下的全部考试的信息

        :return: list of dict, 详情如下
        [{
            'tno': int
            'tname': str
            'pscore': int
            'pnum': int
            'tstart': 时间戳
            'tend': 时间戳
        }]
        """

        tests = Course.get_tests_by_no(cno)

        test_list = []
        for t in tests:
            p = Test.get_paper_by_tno(t.Tno)
            test_list.append({'tno': t.Tno,
                              'tname': t.Tname,
                              'pscore': p.Pscore,
                              'pnum': p.Pnum,
                              'tstart': t.Tstart.timestamp(),
                              'tend': t.Tend.timestamp()})
        return test_list
