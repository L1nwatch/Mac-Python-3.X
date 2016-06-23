#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 矩形覆盖

同样可以参考剑指 Offer (面试题 9)

解题思路摘要:
    可以用 2 * 1 的小矩形横着或者竖着去覆盖更大的矩形。请问用 8 个 2 * 1 的小矩形无重叠地覆盖一个 2 * 8 的大矩形，总共有多少种方法？

    我们先把 2 * 8 的覆盖方法记为 f(8)。用第一个 1 * 2 小矩形去覆盖大矩形的最左边时有两个选择，竖着放或者横着放。
    当竖着放的时候，右边还剩下2 * 7 的区域，这种情况下的覆盖方法记为 f(7)。

    接下来考虑横着放的情况。当 1 * 2 的小矩形横着放在左上角的时候，右下角必须和横着放一个 1 * 2 的小矩形，而在右边还剩下 2 * 6 的区域，
    这种情形下的覆盖方法记为 f(6)，因此 f(8) = f(7) + f(6)。此时可以看出，这仍然是斐波那契数列。
"""

__author__ = '__L1n__w@tch'


def circle_fibonacci(steps, fn_1, fn_2):
    """
    循环求解斐波那契数列, f(n) = f(n - 1) + f(n - 2)
    :param steps: 阶数
    :param fn_1: f(n - 1)
    :param fn_2: f(n - 2)
    :return: f(n)
    """
    for i in range(steps):
        fn_1, fn_2 = fn_2, fn_1 + fn_2
    return fn_2


if __name__ == "__main__":
    n = 3

    print("{} 级台阶: {}".format(n, circle_fibonacci(n, 0, 1)))
