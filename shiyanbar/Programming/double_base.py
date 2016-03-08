#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://www.shiyanbar.com/ctf/1865
求双基回文数

主要是想练一下任意进制转换的代码
'''
__author__ = '__L1n__w@tch'

import gmpy2


def change_base(value, base=10):
    """
    虽然实现了..但是突然发现 gmpy2.digits 已经实现我要的功能了- -
    :param value: 10
    :param base: 2
    :return: 1100100
    """
    number = list()
    while value != 0:
        number.insert(0, value % base)
        value = value // base
    return "".join([str(x) for x in number])


def is_hui_wen(string):
    return string[::-1] == string


def is_double_base_hui_wen(num):
    counts = 0
    for base in range(2, 11):
        string = gmpy2.digits(num, base)
        if is_hui_wen(string):
            counts += 1
        if counts >= 2:
            return True
    return False


def main():
    for num in range(1600000, 10 ** 100):
        if is_double_base_hui_wen(num):
            print(num)
            break


if __name__ == "__main__":
    main()
