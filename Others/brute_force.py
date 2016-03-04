#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 主要是学习了如何遍历 8 位比特的,这个创建爆破(暴力破解)字典之类的会用到
'''
__author__ = '__L1n__w@tch'

import string
import itertools


def create_bytes_iterator(length=8):
    """
    生成器,生成类似于
    b'\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x01'
    b'\x00\x00\x00\x00\x00\x00\x00\x02'
    b'\x00\x00\x00\x00\x00\x00\x00\x03'
    ...
    :param length: 8
    :return: <generator object create_bytes_iterator at 0x??>
    """
    chars = [i for i in range(256)]
    for each in itertools.product(chars, repeat=length):
        yield bytes(each)


def create_dict_iterator(length):
    """
    生成器, 产生字典如a,b,c,...,aa,ab,ac,ad,...,aaa,aab,aac,aad....
    :param length: 3
    :return: a,b,c,...,aa,ab,ac,ad,...,aaa,aab,aac,aad....
    """
    # chars = string.printable[:-6] # -6表示没有空白符
    chars = string.digits + string.ascii_letters
    strings = []
    for i in range(1, length):
        strings.append((itertools.product(chars, repeat=i),))
    for _1 in itertools.chain(*strings):
        for _2 in _1:
            yield "".join(_2)
