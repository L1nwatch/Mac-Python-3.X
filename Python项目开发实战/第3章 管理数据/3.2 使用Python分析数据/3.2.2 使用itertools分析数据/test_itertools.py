#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import itertools as it


def main():
    # count()函数与内置的range()函数的工作原理非常类似。但range()产生有限的数字
    # 而count()从开始点产生无限数字序列。增加的步长可以通过可选参数stepsize控制。
    for n in it.count(15, 2):
        if n < 40:
            print(n, end=" ")
        else:
            break

    # repeat()函数只是持续地或按照指定的次数重复它的参数.
    for n in range(7):
        print(next(it.repeat("yes ")), end=" ")
    print(list(it.repeat(6, 3)))

    # cycle()函数会反复不断地在输入序列上轮转.这对于为负载平衡或资源分配创建轮式迭代是非常有用的
    res1 = list()
    res2 = list()
    res3 = list()
    resources = it.cycle([res1, res2, res3])
    for n in range(30):
        res = next(resources)
        res.append(n)
    print(res1)
    print(res2)
    print(res3)


if __name__ == "__main__":
    main()
