#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Mac OS X 10.10 Python3.4.4下测试locale
'''
__author__ = '__L1n__w@tch'

import locale as loc
import time


def main():
    # 在不同会话中重复这些操作会看到一些差别,系统非常清楚地指定了不同的区域.货币使用了合适的符号
    # 并且日期和时间与UK版本有很大的区别.
    print(loc.setlocale(loc.LC_ALL, ""))
    # print(loc.currency(350)) # 这一句报错了
    print(time.strftime("%x %X", time.localtime()))

    # 示例显示了字符串格式化指定器是如何同时为整数和浮点数工作的.
    print("{:n}".format(3.14159))
    print("{:n}".format(42))

    # locale.strcoll()字符串比较示例是非常有用的,因为它们在字符排序中采用了特定于区域的想法.
    # 如果第一个字符串有更"高"的值,返回值就是1,更低则返回-1,如果两个参数相同,则返回0
    print(loc.strcoll("Spanish", "Inquisition"))
    print(loc.strcoll("Inquisition", "Spanish"))
    print(loc.strcoll("Spanish", "Spanish"))

    # local提供了转换函数,这些函数在特定情况下是很有用的:atoi()、atof()、str()、format()、format_string()


if __name__ == "__main__":
    main()
