#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 古月 Teacher 布置的第一周的 2 个任务之一: 通过文件、IAT或其他方式，提取出恶意代码的 MD5 特征，从而识别恶意代码

参考文章: https://www.fireeye.com/blog/threat-research/2014/01/tracking-malware-import-hashing.html
pefile库-Python2: https://github.com/erocarrera/pefile
pefile库-Python3: https://github.com/simonzack/pefile-py3k

'''
__author__ = '__L1n__w@tch'

import pefile


def main():
    pefile.PE()


if __name__ == "__main__":
    main()
