#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 由于 Python 内置没有带权随机函数(好像是吧?)
'''
__author__ = '__L1n__w@tch'

from random import random
from bisect import bisect


def weighted_choice(choices):
    values, weights = zip(*choices)
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random() * total
    i = bisect(cum_weights, x)
    return values[i]


if __name__ == "__main__":
    for i in range(100):
        print(weighted_choice([("WHITE", 60), ("RED", 30), ("GREEN", 10)]))
