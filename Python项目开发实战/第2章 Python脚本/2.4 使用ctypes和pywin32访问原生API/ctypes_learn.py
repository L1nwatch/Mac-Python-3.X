#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import ctypes as ct


def main():
    libc = ct.cdll.msvcrt  # Windows only
    libc.printf(b"%d %s %s hanging on a wall\n", 6, b"green", b"bottles")
    libc.printf(b"Pi is: %f\n", ct.c_double(3.14159))

    d = ct.c_int()
    print(d.value)
    print(libc.sscanf(b"6",b"%d",ct.byref(d)))
    print(d.value)

    # 这个函数返回Windows系统上一个可用的驱动器列表，这一点使用Python标准库是不容易实现的。
    # 唯一复杂的地方是返回的列表是一个位掩码。


if __name__ == "__main__":
    main()
