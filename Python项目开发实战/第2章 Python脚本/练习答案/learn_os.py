#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 还可以试试os模块的其他函数,例如 os.getpriority()、os.get_exec_path()和os.strerror()等
'''
__author__ = '__L1n__w@tch'

import os


def main():
    print(os.nice(0))  # get relative process priority
    print(os.nice(1))  # change relative priority
    print(os.times())  # process times: system, user etc...
    print(os.isatty(0))  # is the file descriptor arg a tty?(0 = stdin)
    print(os.isatty(4))  # 4 is just an arbitrary test value
    print(os.getloadavg())  # UNIX only - number of processes in queue
    print(os.cpu_count())  # New in Python 3.4


if __name__ == "__main__":
    main()
