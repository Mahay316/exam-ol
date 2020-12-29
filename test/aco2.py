# # coding: utf-8
# from sqlalchemy import CHAR, Column, ForeignKey, Index, Integer, String, TIMESTAMP, Table, text
# from sqlalchemy.dialects.mysql import ENUM, INTEGER, TINYINT
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
# metadata = Base.metadata
#
#
# class Admin(Base):
#     __tablename__ = 'admin'
#
#     Ano = Column(String(20, 'utf8mb4_general_ci'), primary_key=True, comment='管理员账号')
#     Apassword = Column(String(32, 'utf8mb4_general_ci'), nullable=False, comment='管理员密码')
#
#
# class Mentor(Base):
#     __tablename__ = 'mentor'
#
#     Mno = Column(String(20, 'utf8mb4_general_ci'), primary_key=True, comment='教师编号')
#     Mname = Column(String(10, 'utf8mb4_general_ci'), nullable=False, index=True, comment='教师姓名')
#     Mgender = Column(CHAR(1, 'utf8mb4_general_ci'), comment='教师性别')
#     Mtitle = Column(String(10, 'utf8mb4_general_ci'), comment='教师职称')
#     Mpassword = Column(String(32, 'utf8mb4_general_ci'), nullable=False, comment='教师登陆密码')
#
#
# class Student(Base):
#     __tablename__ = 'student'
#
#     Sno = Column(String(20, 'utf8mb4_general_ci'), primary_key=True, comment='学生编号')
#     Sname = Column(String(10, 'utf8mb4_general_ci'), nullable=False, comment='学生姓名')
#     Sgender = Column(ENUM('男', '女'), comment='学生性别')
#     Smajor = Column(String(20, 'utf8mb4_general_ci'), comment='学生专业')
#     Spassword = Column(String(32, 'utf8mb4_general_ci'), nullable=False, comment='学生登陆密码')
#
#
# class Subject(Base):
#     __tablename__ = 'subject'
#
#     Subno = Column(Integer, primary_key=True, comment='科目编号')
#     Subname = Column(String(25, 'utf8mb4_general_ci'), nullable=False, index=True, comment='科目名称')
#
#
# class Course(Base):
#     __tablename__ = 'course'
#
#     Cno = Column(Integer, primary_key=True, comment='课程编号')
#     Cname = Column(String(20, 'utf8mb4_general_ci'), nullable=False, comment='课程名称')
#     Subno = Column(ForeignKey('subject.Subno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='课程所属科目')
#     Mno = Column(ForeignKey('mentor.Mno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='教授该课程教师号')
#
#     mentor = relationship('Mentor')
#     subject = relationship('Subject')
#     student = relationship('Student', secondary='student_course')
#
#
# class Paper(Base):
#     __tablename__ = 'paper'
#
#     Pno = Column(Integer, primary_key=True, comment='试卷的编号')
#     Pname = Column(String(30, 'utf8mb4_general_ci'), index=True, comment='试卷名')
#     Subno = Column(ForeignKey('subject.Subno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='科目编号')
#     Pnum = Column(Integer, nullable=False, comment='试卷包含的题目数量')
#     Pscore = Column(Integer, nullable=False, comment='试卷总分')
#     Preference = Column(Integer, server_default=text("'0'"), comment='试卷被引用的次数')
#     Pisdeleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='真：隐藏 假：显示')
#
#     subject = relationship('Subject')
#
#
# class Question(Base):
#     __tablename__ = 'question'
#     __table_args__ = (
#         Index('Qquery', 'Qno', 'Qtype', 'Qstem', 'Qanswer'),
#     )
#
#     Qno = Column(Integer, primary_key=True, comment='题库中的编号')
#     Qtype = Column(ENUM('select', 'multi', 'fill'), nullable=False, comment='题目类型 select-单选 multi-多选 fill-填空')
#     Qstem = Column(String(255, 'utf8mb4_general_ci'), nullable=False, comment='题目的内容')
#     Qanswer = Column(String(255, 'utf8mb4_general_ci'), nullable=False, comment='JSON列表，题目的答案')
#     Qselect = Column(String(255, 'utf8mb4_general_ci'), comment='JSON列表，选择题的备选项')
#     Subno = Column(ForeignKey('subject.Subno', ondelete='SET NULL', onupdate='CASCADE'), index=True, comment='题目所属的科目')
#     Qreference = Column(INTEGER, nullable=False, server_default=text("'0'"), comment='题目被引用的次数')
#     Qisdeleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='真：隐藏 假：显示')
#
#     subject = relationship('Subject')
#
#
# class QuestionPaper(Base):
#     __tablename__ = 'question_paper'
#
#     Pno = Column(ForeignKey('paper.Pno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, comment='题库中的编号')
#     Qno = Column(ForeignKey('question.Qno', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False, index=True, comment='试卷的编号')
#     QPscore = Column(Integer, server_default=text("'0'"), comment='试题的分值')
#
#     paper = relationship('Paper')
#     question = relationship('Question')
#
#
# t_student_course = Table(
#     'student_course', metadata,
#     Column('Cno', ForeignKey('course.Cno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, comment='课程编号'),
#     Column('Sno', ForeignKey('student.Sno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True, comment='学生编号')
# )
#
#
# class Test(Base):
#     __tablename__ = 'test'
#
#     Tno = Column(Integer, primary_key=True, comment='考试的编号')
#     Tname = Column(String(20, 'utf8mb4_general_ci'), nullable=False, comment='考试的名称')
#     Tdesc = Column(String(255, 'utf8mb4_general_ci'), comment='考试说明')
#     Tstart = Column(TIMESTAMP, nullable=False, comment='考试开始时间')
#     Tend = Column(TIMESTAMP, comment='考试结束时间')
#     Pno = Column(ForeignKey('paper.Pno', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True, comment='引用的试卷编号')
#     Cno = Column(ForeignKey('course.Cno', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True, comment='所属的课程编号')
#
#     course = relationship('Course')
#     paper = relationship('Paper')
#
#
# class StudentTest(Base):
#     __tablename__ = 'student_test'
#
#     Tno = Column(ForeignKey('test.Tno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, comment='考试编号')
#     Sno = Column(ForeignKey('student.Sno', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True, comment='学生编号')
#     STwrong = Column(Integer, comment='错题数量')
#     STblank = Column(Integer, comment='未作答题数')
#     STgrade = Column(Integer, comment='学生考试成绩')
#
#     student = relationship('Student')
#     test = relationship('Test')
