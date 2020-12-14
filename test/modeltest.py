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
from models.QuestionModel import Question

def qt():
    print(Question.is_fill_in_blanks(2))

if __name__ == '__main__':
    qt()
    pass
