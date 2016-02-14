#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 该模块只存在于 Python 3.4或更新版本
'''
__author__ = '__L1n__w@tch'

import statistics as stats


def main():
    print(stats.mean(range(6)))
    print(stats.median(range(6)))
    print(stats.median_low(range(6)))
    print(stats.median_high(range(6)))
    print(stats.median_grouped(range(6)))
    try:
        print(stats.mode(range(6)))
    except Exception as e:
        print(e)
    print(stats.mode(list(range(6)) + [3]))
    print(stats.pstdev(list(range(6)) + [3]))
    print(stats.stdev(list(range(6)) + [3]))
    print(stats.pvariance(list(range(6)) + [3]))
    print(stats.variance(list(range(6)) + [3]))


if __name__ == "__main__":
    main()
