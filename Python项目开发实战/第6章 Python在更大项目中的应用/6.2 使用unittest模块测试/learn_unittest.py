#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 通过创建TestCase类的子类,创建了unittest测试

注意,unittest并不检查一个测试是否被真的执行了.它仅检查是否有异常被抛出.
因此,如果没有异常被抛出,测试被认为OK.这可能意味着你的精确计算在返回的并不是十分精确的值时仍然显示通过或者OK

如果真没有通过测试,如下是三个可能的单元测试的输出:
OK: 测试是OK的,没有抛出异常
Fail: 抛出AssertionError(测试失败)
Error: 抛出非AssertionError异常
'''
__author__ = '__L1n__w@tch'

import unittest


class PythonProjectsTest(unittest.TestCase):
    def test_to_fail(self):
        self.failIf(False)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
