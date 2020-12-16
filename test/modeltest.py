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

def qt():
    t = Test.get_test('t0001')
    for x in t.get_all_questions():
        print(x.Qstem)



if __name__ == '__main__':
    qt()
    pass
