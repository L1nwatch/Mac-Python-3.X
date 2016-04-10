#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 一道题,要求证明存在连续的 n 个整数,可以使得 m + i = 0 (mod pi^2)
所以还是爆破把
'''
__author__ = '__L1n__w@tch'


def main():
    for i in range(10 ** 5):
        if i % 2 ** 2 == 0 \
                and (i + 1) % 3 ** 2 == 0 \
                and (i + 2) % 5 ** 2 == 0 \
                and (i + 3) % 7 ** 2 == 0:
            print(i)
            break


if __name__ == "__main__":
    main()
