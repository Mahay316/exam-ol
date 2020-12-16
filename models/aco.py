# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Table, text
from sqlalchemy.dialects.mysql import ENUM, INTEGER, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Admin(Base):
    __tablename__ = 'admin'

    Ano = Column(String(20, 'utf8mb4_general_ci'), primary_key=True, comment='����Ա�˺�')
    Apassword = Column(String(32, 'utf8mb4_general_ci'), nullable=False, comment='����Ա����')


class Mentor(Base):
    __tablename__ = 'mentor'

    Mno = Column(String(20, 'utf8mb4_general_ci'), primary_key=True, comment='��ʦ���')
    Mname = Column(String(10, 'utf8mb4_general_ci'), nullable=False, comment='��ʦ����')
    Mgender = Column(String(3, 'utf8mb4_general_ci'), comment='��ʦ�Ա�')
    Mtitle = Column(String(10, 'utf8mb4_general_ci'), comment='��ʦְ��')
    Mpassword = Column(String(32, 'utf8mb4_general_ci'), nullable=False, comment='��ʦ��½����')


class Student(Base):
    __tablename__ = 'student'

    Sno = Column(String(20, 'utf8mb4_general_ci'), primary_key=True, comment='ѧ�����')
    Sname = Column(String(10, 'utf8mb4_general_ci'), nullable=False, comment='ѧ������')
    Sgender = Column(ENUM('��', 'Ů'), comment='ѧ���Ա�')
    Smajor = Column(String(20, 'utf8mb4_general_ci'), comment='ѧ��רҵ')
    Spassword = Column(String(32, 'utf8mb4_general_ci'), nullable=False, comment='ѧ����½����')


class Subject(Base):
    __tablename__ = 'subject'

    Subno = Column(VARCHAR(5), primary_key=True, comment='��Ŀ���')
    Subname = Column(VARCHAR(25), nullable=False, comment='��Ŀ����')


class Course(Base):
    __tablename__ = 'course'

    Cno = Column(String(20, 'utf8mb4_general_ci'), primary_key=True, comment='�γ̱��')
    Cname = Column(String(20, 'utf8mb4_general_ci'), nullable=False, comment='�γ�����')
    Subno = Column(ForeignKey('subject.Subno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='�γ�������Ŀ')
    Mno = Column(ForeignKey('mentor.Mno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='���ڸÿγ̽�ʦ��')

    mentor = relationship('Mentor')
    subject = relationship('Subject')
    student = relationship('Student', secondary='student_course')


class Paper(Base):
    __tablename__ = 'paper'

    Pno = Column(String(20, 'utf8mb4_general_ci'), primary_key=True, comment='�Ծ�ı��')
    Pname = Column(String(30, 'utf8mb4_general_ci'), comment='�Ծ���')
    Subno = Column(ForeignKey('subject.Subno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='��Ŀ���')
    Preference = Column(Integer, server_default=text("'0'"), comment='�Ծ����õĴ���')
    Pisdeleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='�棺���� �٣���ʾ')

    subject = relationship('Subject')


class Question(Base):
    __tablename__ = 'question'

    Qno = Column(String(20, 'utf8mb4_general_ci'), primary_key=True, comment='����еı��')
    Qtype = Column(ENUM('select', 'multi', 'fill'), nullable=False, comment='��Ŀ���� select-��ѡ multi-��ѡ fill-���')
    Qstem = Column(String(255, 'utf8mb4_general_ci'), nullable=False, comment='��Ŀ������')
    Qanswer = Column(String(255, 'utf8mb4_general_ci'), nullable=False, comment='JSON��ʽ����Ŀ�Ĵ𰸣�ѡ����ı�ѡ������Ĵ�')
    Qselect = Column(String(10, 'utf8mb4_general_ci'), comment='ѡ�������ȷѡ��')
    Subno = Column(ForeignKey('subject.Subno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='��Ŀ�����Ŀ�Ŀ')
    Qreference = Column(INTEGER, nullable=False, server_default=text("'0'"), comment='��Ŀ�����õĴ���')
    Qisdeleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='�棺���� �٣���ʾ')

    subject = relationship('Subject')


class QuestionPaper(Base):
    __tablename__ = 'question_paper'

    Pno = Column(ForeignKey('paper.Pno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, comment='����еı��')
    Qno = Column(ForeignKey('question.Qno', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False, index=True, comment='�Ծ�ı��')
    QPscore = Column(Integer, server_default=text("'0'"), comment='����ķ�ֵ')
    QPposition = Column(Integer, comment='��Ŀ���Ծ��е�λ��')

    paper = relationship('Paper')
    question = relationship('Question')


class student_course(Base):
    'student_course', metadata,
    Column('Cno', ForeignKey('course.Cno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, comment='�γ̱��'),
    Column('Sno', ForeignKey('student.Sno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True, comment='ѧ�����')



class Test(Base):
    __tablename__ = 'test'

    Tno = Column(VARCHAR(20), primary_key=True, comment='���Եı��')
    Tname = Column(VARCHAR(20), nullable=False, comment='���Ե�����')
    Tstart = Column(TIMESTAMP, nullable=False)
    Tend = Column(TIMESTAMP)
    Pno = Column(ForeignKey('paper.Pno', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True, comment='���õ��Ծ���')
    Cno = Column(ForeignKey('course.Cno', ondelete='RESTRICT', onupdate='CASCADE'), index=True, comment='�����Ŀγ̱��')

    course = relationship('Course')
    paper = relationship('Paper')


class StudentTest(Base):
    __tablename__ = 'student_test'

    Tno = Column(ForeignKey('test.Tno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, comment='���Ա��')
    Sno = Column(ForeignKey('student.Sno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True, comment='ѧ�����')
    STgrade = Column(Integer, comment='ѧ�����Գɼ�')

    student = relationship('Student')
    test = relationship('Test')
