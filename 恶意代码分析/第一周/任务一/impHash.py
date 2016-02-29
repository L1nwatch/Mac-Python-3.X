#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 古月 Teacher 布置的第一周的 2 个任务之一: 通过文件、IAT或其他方式，提取出恶意代码的 MD5 特征，从而识别恶意代码

参考文章: https://www.fireeye.com/blog/threat-research/2014/01/tracking-malware-import-hashing.html
pefile库-Python2: https://github.com/erocarrera/pefile
pefile库-Python3: https://github.com/XeroNicHS/pefile_py3

实现思路有 2 个:
第一个直接调用 pefile 库的 get_imphash() 实现
第二个是根据给定的 rva 范围, 对文件对应的 rva 范围字节流进行哈希
'''
__author__ = '__L1n__w@tch'

import pefile
import hashlib


def get_imphash():
    """
    仅仅是测试一下如何调用 pefile 库来获取 imphash
    :return:
    """
    pe = pefile.PE("Lab06-02.exe")
    print(pe.get_imphash())


def get_hash(file_name):
    file_name = "Lab06-02.exe"
    with open(file_name, "rb") as f:
        data = f.read()
        print(len(data))


def main():
    file_name = ""

    get_imphash()
    get_hash(None)
    # get_hash(rva_start, rva_end)


if __name__ == "__main__":
    main()
