#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 变态台阶问题, 一只青蛙一次可以跳上 1 级台阶, 也可以跳上 2 级, 它也可以跳上 n 级. 求该青蛙跳上一个 n 级的台阶总共有多少种跳法

根据数学归纳法可证得答案为 2 ^ n - 1 (可参考剑指 Offer 面试题 9)
"""

__author__ = '__L1n__w@tch'


def recursion(steps):
    if steps < 2:
        return steps
    else:
        return 2 * recursion(steps - 1)


if __name__ == "__main__":
    n = 233
    print("{} 级台阶: {}".format(n, recursion(n)))

    compute_jump = lambda steps: steps if steps < 2 else 2 * compute_jump(steps - 1)
    print("{} 级台阶: {}".format(n, compute_jump(n)))
