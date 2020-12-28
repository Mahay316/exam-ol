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


def qt():
    # print(Question.add_question(qtype='select', qstem='aaaa', qanswer='sdsd', qselect='BD', qsubject='软件工程'))

    # print(Course.add_class_member('c0003','student1'))

    # print(Course.del_class_member('c0001','student2'))

    

    pass


def fg():
    s = Question.select_questions_by(page=3, content='这是')
    for x in s:
        print(x.Qno)


if __name__ == '__main__':
    qt()
    # fg()
    pass
