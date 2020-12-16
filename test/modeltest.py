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

def qt():
    print(Test.get_all_question_id('t01'))



if __name__ == '__main__':
    qt()
    pass
