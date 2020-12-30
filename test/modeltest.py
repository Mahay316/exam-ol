#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/14 23:43
# @Author  : kiwanter
# @Email   : kiwanter@163.com
# @File    : modeltest.py
# @software: pycharm

'''
@file function:
'''

from models import Course
from models import StudentTest
from models import Subject
from models import Question
from common import model_common
from models import Paper
from models import Test
from models import Mentor
from models.UserModel import Student


def qt():

    # print(Student.has_this_class('student3',4))
    # s = Student.get_user('student1')
    # print(Student.get_all_test_ids(s))
    # print(Student.get_classes('student1'))
    # print(Question.add_question(qtype='select', qstem='aaaa', qanswer='sdsd', qselect='BD', qsubject='软件工程'))

    # print(Course.add_class_member('c0003','student1'))

    # print(Course.del_class_member('c0001','student2'))

    # q = Question.select_questions_by(content='这是',qno='q00002')
    # for x in q:
    #     print(x.Qno)

    # q = True
    #
    # if q == None:
    #     print('1')
    #
    # elif q == False:
    #     print('2')
    #
    # elif q == True:
    #     print('3')

    # ps = Paper.select_papers_by(pname='数据',subject='s0002')
    # for x in ps:
    #     print(x.Pno)

    # s = Subject.get_all_subs()
    # print(s)

    # Question.delete_question('q00002')

    # Question.add_question('select','aaa','wewew','ewew','s0002')

    # Paper.delete_paper('p0004')
    #
    # print(Paper.get_paper_num())

    # Question.delete_question('q00003')
    #
    # print(Question.get_question_num())

    pass


def fg():
    # s = Question.select_questions_by(page=3, content='这是')
    # for x in s:
    #     print(x.Qno)

    # print(Question.update_question('q00004','fill','www','rere','B','s0001'))

    # l = Question.get_questions_by_pno('p0001')
    # for x in l:
    #     print(x.Qstem)
    # pass

    # print(Question.get_question_num())

    # t = Test.get_test('1')
    # l = Test.get_all_questions(t)
    #
    # for x in l:
    #     print(str(x[0].Qno) + ' ' + str(x[1]))

    # Question.add_question('select','qwwqw','wewewew','ew','2')

    # qs = [{'qno': 1, 'qpscore': 3},
    #  {'qno': 2, 'qpscore': 4},
    #  {'qno': 3, 'qpscore': 10}]
    # print(Paper.add_paper(questions=qs, pname='testp', subno=3))

    # print(Test.get_paper_by_tno(2).Pname)

    # print(Test.set_test_grade(2,'student',4,2,77))

    #print(Mentor.get_classes('teacher1_en'))

    #print(Course.get_tests_by_no(4)[0].Tno)

    # for x in Course.get_students_by_no(4):
    #     print(x.Sno)

    # for x in Course.get_exams_by_cno(4):
    #     print(x.Tno)

    print(Course.get_test_info_by_cno(4))

    # Ste
    pass


if __name__ == '__main__':
    qt()
    # fg()
    pass
