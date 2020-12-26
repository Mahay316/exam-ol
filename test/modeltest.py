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

from models import Paper
from models import Test
from models import Question
from models import Student

def qt():
    x = Student.get_user('student3')
    print(x.get_all_test_ids())



if __name__ == '__main__':
    qt()
    pass
