#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Mac OS X 10.10 Python3.4.4下测试unicode相关细节以及unicodedata模块
'''
__author__ = '__L1n__w@tch'

import unicodedata as ud


def main():
    # 可以在字面量字符串中使用Unicode字符,甚至可以使用它们的长名字
    print("A")
    print("\u0041")
    print("\N{LATIN CAPITAL LETTER A}")

    # 可以使用字符串的encode()方法来获得用于存储数据的原生字节
    print("\u00A1Help!")
    print("\u00A1Help!".encode("utf-8"))
    print(b"\xc2\xa1Help!".decode("utf-8"))

    # unicodedata模块,它在交互式提示符中是非常有用的.它可以作为一种找到关于Unicode字符的方式.
    # 通过使用unicodedata模块,可以得到一个给定字符的Unicode名字和类别.然后根据这些可以在网站查到更多细节.
    # 可以试着对字节字符串进行解码,来检查塔是否是有效的UTF-8
    data = b"\xd9\x85\xd8\xb1\xd8\xad\xd8\xa8\xd8\xa7\xd8\xa3\xd9\x84\xd8\xa7\xd9\x86"
    print(data.decode("utf-8"))
    # 从ud.name()打印出来的消息来看,这是阿拉伯语
    for ch in data.decode("utf-8"):
        print(ord(ch), ud.name(ch))


if __name__ == "__main__":
    main()
