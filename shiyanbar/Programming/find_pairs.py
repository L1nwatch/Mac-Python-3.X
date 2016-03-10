#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://www.shiyanbar.com/ctf/1859
题目描述: 1/400=1/x+1/2y，(x>y)。你的任务就是求出共有多少对这样的正整数x和y，使得该等式成立。
x > 400
600 > y > 200

学一下 Python 的分数库啊!!!
'''
__author__ = '__L1n__w@tch'

import fractions


def compute_x(y):
    x = fractions.Fraction(1, 400) - fractions.Fraction(1, 2 * y)
    if x.numerator == 1: # 分母是 x.denominator
        return x
    else:
        return None


def main():
    pairs = set()

    for y in range(201, 600):
        x = compute_x(y)
        if x:
            pairs.add((x, y))

    print(len(pairs))
    print(pairs)


if __name__ == "__main__":
    main()
