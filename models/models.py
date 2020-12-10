# coding: utf-8
from sqlalchemy import CHAR, Column, ForeignKey, Integer, String, TIMESTAMP, Table, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Admin(Base):
    __tablename__ = 'admin'

    Ano = Column(String(20), primary_key=True, comment='管理员账号')
    Apassword = Column(String(20), nullable=False, comment='管理员密码')


class Mentor(Base):
    __tablename__ = 'mentor'

    Mno = Column(String(20), primary_key=True, comment='教师编号')
    Mname = Column(String(10), nullable=False, comment='教师姓名')
    Mgender = Column(String(3), comment='教师性别')
    Mtitle = Column(String(10), comment='教师职称')
    Mpassword = Column(String(20), nullable=False, comment='教师登陆密码')


class Student(Base):
    __tablename__ = 'student'

    Sno = Column(String(20), primary_key=True, comment='学生编号')
    Sname = Column(String(10), nullable=False, comment='学生姓名')
    Sgender = Column(VARCHAR(3), comment='学生性别')
    Smajor = Column(String(20), comment='学生专业')
    Spassword = Column(String(20), nullable=False, comment='学生登陆密码')


class Subject(Base):
    __tablename__ = 'subject'

    Subno = Column(String(20), primary_key=True, comment='科目编号')
    Subname = Column(String(25), nullable=False, comment='科目名称')


class Course(Base):
    __tablename__ = 'course'

    Cno = Column(String(20), primary_key=True, comment='课程编号')
    Cname = Column(String(20), nullable=False, comment='课程名称')
    Subno = Column(ForeignKey('subject.Subno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='课程所属科目')
    Mno = Column(ForeignKey('mentor.Mno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='教授该课程教师号')

    mentor = relationship('Mentor')
    subject = relationship('Subject')
    student = relationship('Student', secondary='student_course')


class Paper(Base):
    __tablename__ = 'paper'

    Pno = Column(String(20), primary_key=True, comment='试卷的编号')
    Pname = Column(String(30), comment='试卷名')
    Preference = Column(Integer, server_default=text("'0'"), comment='试卷被引用的次数')
    Pisdeleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='真：隐藏 假：显示')
    Subno = Column(ForeignKey('subject.Subno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='科目编号')

    subject = relationship('Subject')


class Question(Base):
    __tablename__ = 'question'

    Qno = Column(String(20), primary_key=True, comment='题库中的编号')
    Qtype = Column(TINYINT(1), nullable=False, comment='题目类型')
    Qstem = Column(String(255), nullable=False, comment='题目的内容')
    Qanswer = Column(String(255), nullable=False, comment='题目的正确答案，由字典转化的字符串')
    Qselect = Column(TINYINT(1), comment='选择题的正确选项')
    Subno = Column(ForeignKey('subject.Subno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='题目所属的科目')
    Qreference = Column(INTEGER, nullable=False, server_default=text("'0'"), comment='题目被引用的次数')
    Qisdeleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='真：隐藏 假：显示')

    subject = relationship('Subject')


class QuestionPaper(Base):
    __tablename__ = 'question_paper'

    Pno = Column(ForeignKey('paper.Pno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, comment='题库中的编号')
    Qno = Column(ForeignKey('question.Qno', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False, index=True, comment='试卷的编号')
    QPscore = Column(Integer, server_default=text("'0'"), comment='试题的分值ֵ')
    QPposition = Column(Integer, comment='题目在试卷中的位置')

    paper = relationship('Paper')
    question = relationship('Question')


class StudentCourse:
    __tablename__ = 'student_course'
    Column('Cno', ForeignKey('class.Cno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, comment='课程编号'),
    Column('Sno', ForeignKey('student.Sno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True, comment='课程编号')

    course = relationship('Course')
    student = relationship('Student')

class Test(Base):
    __tablename__ = 'test'

    Tno = Column(CHAR(20), primary_key=True, comment='考试的编号')
    Tname = Column(VARCHAR(20), nullable=False, comment='考试的名称')
    Tstart = Column(TIMESTAMP, nullable=False, comment='考试开始时间')
    Tend = Column(TIMESTAMP, comment='考试结束时间')
    Pno = Column(ForeignKey('paper.Pno', ondelete='RESTRICT', onupdate='CASCADE'), index=True, comment='引用的试卷编号')
    Cno = Column(ForeignKey('class.Cno', ondelete='RESTRICT', onupdate='CASCADE'), index=True, comment='所属的课程编号')

    course = relationship('Course')
    paper = relationship('Paper')


class StudentTest(Base):
    __tablename__ = 'student_test'

    Tno = Column(ForeignKey('test.Tno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, comment='考试编号')
    Sno = Column(ForeignKey('student.Sno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True, comment='学生编号')
    STgrade = Column(Integer, comment='学生考试成绩')

    student = relationship('Student')
    test = relationship('Test')
