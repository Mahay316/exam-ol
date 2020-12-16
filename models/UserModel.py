from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import relationship

from models.database import Base
from common import model_common
from common.Role import *
from models.StudentTestModel import StudentTest


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

    def has_this_Test(self, test):
        """
        返回该学生是否有本次考试
        :return True or False
        """

        Tnos = []
        for t in self.studenttest:
            Tnos.append(t.Tno)

        if test.Tno in Tnos:
            return True
        else:
            return False


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


class Mentor(User, Base):
    __tablename__ = 'mentor'

    Mno = Column(String(20, 'utf8mb4_general_ci'), primary_key=True, comment='教师编号')
    Mname = Column(String(10, 'utf8mb4_general_ci'), nullable=False, comment='教师姓名')
    Mgender = Column(String(3, 'utf8mb4_general_ci'), comment='教师性别')
    Mtitle = Column(String(10, 'utf8mb4_general_ci'), comment='教师职称')
    Mpassword = Column(String(32, 'utf8mb4_general_ci'), nullable=False, comment='教师登陆密码')

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
