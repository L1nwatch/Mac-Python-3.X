#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 快速指数算法
x^a mod n = x^(ak * 2^k + ak-1 * 2^(k-1) + ... + a1 * 2 + a0)

输入: 整数 x, a > 0, n > 1
输出: x^a mod n
'''
__author__ = '__L1n__w@tch'


def fast_multiplcation(x, a, n):
    """
    快速指数算法
    x^a mod n = x^(ak * 2^k + ak-1 * 2^(k-1) + ... + a1 * 2 + a0)
    :param x: int
    :param a: a > 0
    :param n: n > 1
    :return: x^a mod n
    """
    assert type(x) == int
    assert a > 0
    assert n > 1

    a = bin(a)[2:][::-1]
    y, i = 1, len(a) - 1
    while i >= 0:
        y = y * y % n
        if a[i] == "1":
            y = y * x % n
        i -= 1
    return y


def main():
    ans = fast_multiplcation(21, 39, 100)
    print(ans)


if __name__ == "__main__":
    main()
