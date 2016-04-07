#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 课本专门用了 1.4 节来介绍 Euclid 基本算法和扩展算法, 其中介绍了两个具体实现, 第一个实现是计算最大公约数,
第二个实现是求 (a,b)=a*x0 + b*y0, 于是用 Python 来具体实现了.
'''
__author__ = '__L1n__w@tch'

import gmpy2


def gcd(a, b):
    a, b = max(a, b), min(a, b)
    x, y = a, b
    while y != 0:
        r = x % y
        x = y
        y = r
    return x


def gcdext(a, b):
    """
    gcdext(330, -210)
    :param a:
    :param b:
    :return:
    """
    assert a > b >= 0
    x1, x2, x3 = 1, 0, a
    y1, y2, y3 = 0, 1, b
    while y3 != 0:
        q = x3 // y3
        t1, t2, t3 = x1 - q * y1, x2 - q * y2, x3 - q * y3
        x1, x2, x3 = y1, y2, y3
        y1, y2, y3 = t1, t2, t3
    return x3, x1, x2


def main():
    assert gmpy2.gcd(2108, 3720) == gcd(2108, 3720)
    assert gmpy2.gcdext(3720, 2108) == gcdext(3720, 2108)
    print(gmpy2.gcdext(210, -330))
    # assert gmpy2.gcdext(330, -210) == gcdext(330, -210)


if __name__ == "__main__":
    main()
