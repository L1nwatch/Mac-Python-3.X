#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 当编写测试时,只是创建了一些静态数据,这些数据会被传入到已经定义的函数中.
你想要向函数传入一个已知的值,然后在测试中展示期待得到的返回值.如果那个值没有被返回,测试应该会失败.
如果值返回了,测试会通过,并且代码会转向下一个测试函数

程序中的一个函数可能有多个测试,或者一个测试验证多种情况
'''
__author__ = '__L1n__w@tch'

import unittest
from example import first, last

list_nums = [7, 9, 5]
list_chars = ['m', 'd', 'Z', 'l']


class TestPPMath(unittest.TestCase):
    # 记住,想要运行的所有测试函数必须以test开头
    def test_first(self):
        # 这个测试应该会通过,因为当你对数字列表排序时,列表中的第一个元素是5,所以这应该会返回真
        self.assertEqual(first(list_nums), 5)

    # 类似于检查相等性的AssertEqual,还有一个assertTrue.它会检查第一个值是否是第二个值,如果是,则为真:
    def test_last(self):
        self.assertTrue(last(list_chars), "m")

    # unittest只会寻找异常,比如assertionError异常.可以使用failUnless()函数来告诉塔,除非它返回真,否则测试失败
    def test_first_again(self):
        self.failUnless(first(list_chars), "Z")

    # 如果想要在它是真时让测试失败,可以使用failIf()函数.它在输入被认为是真时失败.所以,这个测试在运行时应该会失败
    def test_last_again(self):
        self.failIf(last(list_nums), 9)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
