#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 测试自己写的函数是否正确
"""
from create_date import is_leap_year
import unittest
import calendar

__author__ = '__L1n__w@tch'


class Test(unittest.TestCase):
    def test_leap_year(self):
        for i in range(-3000, 3000):
            self.failIf(is_leap_year(i, learn=True) != calendar.isleap(i))


if __name__ == "__main__":
    pass
