#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import ctypes as ct
import string


def main():
    under_windows()
    under_linux()


def under_windows():
    libc = ct.cdll.msvcrt  # Windows only
    libc.printf(b"%d %s %s hanging on a wall\n", 6, b"green", b"bottles")
    libc.printf(b"Pi is: %f\n", ct.c_double(3.14159))

    d = ct.c_int()
    print(d.value)
    print(libc.sscanf(b"6", b"%d", ct.byref(d)))
    print(d.value)

    # msvcrt_getdrives()函数返回Windows系统上一个可用的驱动器列表，这一点使用Python标准库是不容易实现的。
    # 唯一复杂的地方是返回的列表是一个位掩码。
    drives = string.ascii_uppercase
    drive_list = libc._getdrives()
    for n in range(26):
        mask = 1 << n  # use left bit shifting to build a mask
        if drive_list & mask:
            print(drives[n], "is available")


def under_linux():
    libc = ct.CDLL("libc.so.6")
    libc.printf(b"My name is %s\n", b"Fred")


if __name__ == "__main__":
    main()
