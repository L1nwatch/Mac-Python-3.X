#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 需要练习一下单元测试的相关知识

本文件是对同文件夹下的 fibonacci 几种写法进行测试
"""
import unittest
from fibonacci import recursion, memory_recursion, circle

__author__ = '__L1n__w@tch'


class FibonacciTest(unittest.TestCase):
    def setUp(self):
        self.wait_to_test = [recursion, memory_recursion, circle]  # 待测试的函数

    def normal_test(self):
        """
        简单的功能性测试罢了
        :return:
        """
        for function in self.wait_to_test:
            self.failUnless(function(1) == 1)
            self.failUnless(function(2) == 2)
            self.failUnless(function(3) == 3)
            self.failUnless(function(4) == 5)
            self.failUnless(function(5) == 8)
            self.failUnless(function(6) == 13)
            self.failUnless(function(7) == 21)
            self.failUnless(function(13) == 377)
            self.failUnless(function(15) == 987)
            self.failUnless(function(20) == 10946)
            self.failUnless(function(25) == 121393)
            self.failUnless(function(29) == 832040)
            self.failUnless(function(33) == 5702887)
            if function.__name__ == "recursion":
                print("递归 50 次时间太长, 不测试了")
                continue
            self.failUnless(function(50) == 20365011074)
            print("函数: {}, 测试完毕".format(function.__name__))


if __name__ == "__main__":
    unittest.main()
