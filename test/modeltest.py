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

def qt():
    x = StudentTest.get_st_by_tno('t0001')
    print(x)

def fg():
    x=Course.get_class('c0001')
    print(x.Cname)


if __name__ == '__main__':
    qt()
    # fg()
    pass
