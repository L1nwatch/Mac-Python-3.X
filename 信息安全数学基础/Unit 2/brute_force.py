#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 要求找到模 9 和模 10 的两个完全剩余系, 要求其中一个完系中全为奇数, 另一个全为偶数
'''
__author__ = '__L1n__w@tch'


def get_full_series(num, upper_bound=10 ** 5):
    odd_set = set()
    even_set = set()

    for i in range(10 ** 5):
        # even_set
        if i % 2 == 0:
            if i % num not in even_set:
                even_set.add(i)
        # odd_set
        else:
            if i % num not in odd_set:
                odd_set.add(i)
        if len(odd_set) == num and len(even_set) == num:
            break
    return (odd_set, even_set)


def main():
    series_9 = get_full_series(9)
    print("{}: {}".format(9, series_9))

    series_10 = get_full_series(10)
    print("{}: {}".format(10, series_10))


if __name__ == "__main__":
    main()
