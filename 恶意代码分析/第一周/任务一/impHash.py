#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 古月 Teacher 布置的第一周的 2 个任务之一: 通过文件、IAT或其他方式，提取出恶意代码的 MD5 特征，从而识别恶意代码

参考文章: https://www.fireeye.com/blog/threat-research/2014/01/tracking-malware-import-hashing.html
pefile库-Python2: https://github.com/erocarrera/pefile
pefile库-Python3: https://github.com/XeroNicHS/pefile_py3

实现有 4 个:
第一个直接调用 hashlib 库中的 md5 对整个文件进行哈希
第二个直接调用 pefile 库的 get_imphash() 实现
第三个是直接哈希每一个节
第四个是根据给定的 offset 范围, 对文件对应的 offset 范围字节流进行哈希
'''
__author__ = '__L1n__w@tch'

import pefile
import hashlib


def hash_file(file_name="Lab06-02.exe"):
    """对整个文件进行哈希"""
    with open(file_name, "rb") as f:
        data = f.read()
    print(hashlib.md5(data).hexdigest())


def imphash(file_name="Lab06-02.exe"):
    """
    仅仅是测试一下如何调用 pefile 库来获取 imphash
    :return:
    """
    pe = pefile.PE(file_name)
    print(pe.get_imphash())


def hash_offset(file_name="Lab06-02.exe"):
    """根据给定的 offset 范围, 对文件对应的 offset 范围字节流进行哈希"""
    with open(file_name, "rb") as f:
        data = f.read()

    offset = input("Filename = {}, please input offset range (such as 64DC,6504): ".format(file_name))
    offset_start, offset_end = offset.split(",")
    data = data[int(offset_start, 16):int(offset_end, 16)]
    print(hashlib.md5(data).hexdigest())


def hash_section(file_name="Lab06-02.exe"):
    """
    对每个节都进行哈希
    :param file_name:
    :return:
    """
    pe = pefile.PE(file_name)
    for each in pe.sections:
        print(each.Name)  # 打印出所哈希节的名称
        print(hashlib.md5(str(each).encode("utf-8")).hexdigest())  # 对该节进行哈希


def main():
    file_name = "Lab06-02.exe"
    hash_file(file_name)
    imphash(file_name)
    hash_section()
    hash_offset(file_name)


if __name__ == "__main__":
    main()
