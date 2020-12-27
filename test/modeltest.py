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

def qt():
    qs = Question.select_questions_by(content='多选')
    for q in qs:
        print(q.Qno)

def fg():
    x=Course.get_class('c0001')
    print(x.Cname)


if __name__ == '__main__':
    qt()
    # fg()
    pass
