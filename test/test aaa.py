#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 上午12:50
# @Author  : kiwanter
# @Email   : kiwanter@163.com
# @File    : test aaa.py
# @software: pycharm

'''
@file function:
'''

from models import *

def fun():

    print(Test.delete_test(6))
    # print(Test.get_student_test_info(6, 120181080102))
    # print(Question.get_question_num())
    # for x in Question.get_questions_by_qnos([1, 3, 4, 5, 6]):
    #     print([x.Qno, x.Qstem, x.Qtype])
    # print(Question.get_questions_by_pno(1))

    # x = Paper.delete_paper(5)
    # print(x)

if __name__ == '__main__':
    fun()