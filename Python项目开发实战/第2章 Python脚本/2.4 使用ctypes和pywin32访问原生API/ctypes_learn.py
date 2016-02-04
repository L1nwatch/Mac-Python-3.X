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


if __name__ == "__main__":
    main()
