from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import relationship

from models.database import Base
from common import model_common
from common.Role import *
from models.StudentTestModel import StudentTest
from models.StudentCourseModel import StudentCourse
from models.CourseModel import Course


class User:

    def is_mentor(self):
        return isinstance(self, Mentor)

    def is_student(self):
        return isinstance(self, Student)

    def is_admin(self):
        return isinstance(self, Admin)

    def verify_password(self, password: str) -> bool:
        """
        根据不同子类从不同表中查询
        """
        if isinstance(self, Student):
            if self.Spassword == password:
                return True
            else:
                return False
        elif isinstance(self, Mentor):
            if self.Mpassword == password:
                return True
            else:
                return False
        else:
            if self.Apassword == password:
                return True
            else:
                return False

    @classmethod
    def get_user(cls, no):
        """
        抽象方法，根据id获取user
        :param no:
        :return:
        """
        raise NotImplementedError

    @classmethod
    def get_user_by_role(cls, no, role):
        """
        通过指明身份来获取用户
        :return: 对应子类
        """

        try:

            if role == STUDENT:
                return Student.get_user(no)
            elif role == MENTOR:
                return Mentor.get_user(no)
            elif role == ADMIN:
                return Admin.get_user(no)
            else:
                raise Exception("没有此种身份")

        except Exception as e:
            raise e


class Student(User, Base):
    __tablename__ = 'student'

    Sno = Column(String(20, 'utf8mb4_general_ci'), primary_key=True, comment='学生编号')
    Sname = Column(String(10, 'utf8mb4_general_ci'), nullable=False, comment='学生姓名')
    Sgender = Column(ENUM('男', '女'), comment='学生性别')
    Smajor = Column(String(20, 'utf8mb4_general_ci'), comment='学生专业')
    Spassword = Column(String(32, 'utf8mb4_general_ci'), nullable=False, comment='学生登陆密码')

    studenttest = relationship('StudentTest', backref='student')
    studentcourse = relationship('StudentCourse', backref='student')

    #  (之前使用flask_login.current_user判定学生是否含有本次考试，现由于使用session实现登录,
    #  使用新的get_all_test_ids方法实现该操作)
    # def has_this_Test(self, test):
    #     """
    #     返回该学生是否有本次考试
    #     :return True or False
    #     """
    #
    #     Tnos = []
    #     for t in self.studenttest:
    #         Tnos.append(t.Tno)
    #
    #     if test.Tno in Tnos:
    #         return True
    #     else:
    #         return False

    def get_all_test_ids(self):
        """
        学生对象调用此方法，返回该学生含有的所有考试id号

        :return: list[str]
        """
        Tnos = []
        for t in self.studenttest:
            Tnos.append(t.Tno)
        return Tnos

    @classmethod
    def get_user(cls, no):
        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Sno == no)

            user = session.query(cls).filter(*filter_list).first()
            return user

        except Exception as e:
            session.rollback()
            raise e

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def get_classes(cls, no) -> list:
        """
        获取某学生的全部课程对象

        :param no: 学号
        :return: list[Course](没有课程则返回空列表)
        """

        classes = []

        try:
            student = Student.get_user(no)
            if not student:
                raise Exception('没有该学生号记录')
            for sc in student.studentcourse:
                course = Course.get_class(sc.Cno)
                classes.append(course)
            return classes

        except Exception as e:
            raise e

    @classmethod
    def has_this_class(cls, student_no, course_no):
        """
        判断学生是否有某门课程

        :return: True or False
        """

        try:
            student = Student.get_user(student_no)
            if not student:
                raise Exception('没有该学生号记录')
            for sc in student.studentcourse:
                if course_no == sc.Cno:
                    return True
            return False

        except Exception as e:
            raise e


class Mentor(User, Base):
    __tablename__ = 'mentor'

    Mno = Column(String(20, 'utf8mb4_general_ci'), primary_key=True, comment='教师编号')
    Mname = Column(String(10, 'utf8mb4_general_ci'), nullable=False, comment='教师姓名')
    Mgender = Column(String(3, 'utf8mb4_general_ci'), comment='教师性别')
    Mtitle = Column(String(10, 'utf8mb4_general_ci'), comment='教师职称')
    Mpassword = Column(String(32, 'utf8mb4_general_ci'), nullable=False, comment='教师登陆密码')

    course = relationship('Course', backref='mentor')

    @classmethod
    def get_user(cls, no):
        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Mno == no)

            user = session.query(cls).filter(*filter_list).first()
            return user

        except Exception as e:
            session.rollback()
            raise e

        finally:
            engine.dispose()
            session.remove()

    @classmethod
    def get_classes(cls, no) -> list:
        """
        获取某教师的全部课程对象

        :param no: 教师号
        :return: list[Course](没有课程则返回空列表)
        """

        try:
            mentor = Mentor.get_user(no)
            if not mentor:
                raise Exception('没有该教师号记录')
            return mentor.course

        except Exception as e:
            raise e

    @classmethod
    def has_this_class(cls, mentor_no, course_no):
        """
        判断老师是否有某门课程

        :return: True or False
        """
        try:
            classes = Mentor.get_classes(mentor_no)
            for course in classes:
                if course_no == course.Cno:
                    return True
            return False

        except Exception as e:
            raise e


class Admin(User, Base):
    __tablename__ = 'admin'

    Ano = Column(String(20, 'utf8mb4_general_ci'), primary_key=True, comment='管理员账号')
    Apassword = Column(String(32, 'utf8mb4_general_ci'), nullable=False, comment='管理员密码')

    @classmethod
    def get_user(cls, no):
        engine = model_common.get_mysql_engine()
        session = model_common.get_mysql_session(engine)

        try:
            filter_list = []
            filter_list.append(cls.Ano == no)

            user = session.query(cls).filter(*filter_list).first()
            return user

        except Exception as e:
            session.rollback()
            raise e

        finally:
            engine.dispose()
            session.remove()
