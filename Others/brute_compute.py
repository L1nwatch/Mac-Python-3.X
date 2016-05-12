#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' jh 的一道题, 要求计算 8 ? 4 ? 6 == 6 ? 7 ? 4, 只有三个数还好说, 十个数呢?于是用 Python 大法了
'''
__author__ = '__L1n__w@tch'

import itertools


def create_operation_list(operations):
    """
    Python 强大的生成器
    :param operations: ["+", "-", "*", "/"]
    :return: ++++, +++-, +++*, +++/, ++-+, ++--, ...
    """
    strings = []
    for i in range(len(operations), len(operations) + 1):
        strings.append((itertools.product(operations, repeat=i),))
    for _1 in itertools.chain(*strings):
        for _2 in _1:
            yield "".join(_2)


if __name__ == "__main__":
    operations = ["+", "-", "*", "/"]

    operation_list = create_operation_list(operations)

    for operation in operation_list:
        if eval("8{}4{}6==6{}7{}4".format(operation[0], operation[1], operation[2], operation[3])):
            print("8{}4{}6==6{}7{}4".format(operation[0], operation[1], operation[2], operation[3]))
            break
