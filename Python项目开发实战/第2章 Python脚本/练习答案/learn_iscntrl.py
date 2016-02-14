#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 迭代前 128 字符并显示一个消息,表示值是否是一个控制字符(其序数值在 0x00 和 0x1F 之间以及 0x7F 的字符).
使用 ctypes 访问标准C库并调用 iscntrl() 函数来确定,注意,该函数并非 Python 中字符串类型的内置测试函数
'''
__author__ = '__L1n__w@tch'

import ctypes as ct


def main():
    # libc = ct.CDLL("libc.so.6")  # in Linux
    libc = ct.cdll.msvcrt  # in Windows

    for c in range(128):
        print(c, " is a ctrl char" if libc.iscntrl(c) else " is not a ctrl char")


if __name__ == "__main__":
    main()
