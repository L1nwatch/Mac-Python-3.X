#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://www.shiyanbar.com/ctf/1807
问题描述:
6ac66ed89ef9654cf25eb88c21f4ecd0是flag的MD5码，（格式为ctf{XXX_XXXXXXXXXXX_XXXXX}）由一个0-1000的数字，下划线，纽约的一个区，
下划线，一个10000-15000的数字构成。

学一下 format 转义的问题,如果要同时打印 {} 就用 {{}},如果只想打印左边的话就用{{,如果只想打印右边的话就用}}
坑了,跑了一趟没跑出来,看了 wp 才知道要连同 ctf 格式进行哈希才行
'''
__author__ = '__L1n__w@tch'

from Crypto.Hash import MD5
import hashlib


def get_flag():
    flag = str()
    # 这个看 wp 的
    boroughs = ['thebronx', 'brooklyn', 'manhattan', 'queens', 'richmond', 'statenisland']
    for prefix in range(0, 1000):
        for borough in boroughs:
            for suffix in range(10000, 15000):
                flag = "ctf{{{}_{}_{}}}".format(str(prefix).zfill(3), borough, suffix)
                hash = MD5.new(flag.encode("utf8")).hexdigest()  # 原来如此,多此一举了,以为有 0x 在最前面
                if hash == "6ac66ed89ef9654cf25eb88c21f4ecd0":
                    return flag


def test():
    """
    又是遇到了 Crypto.Hash 中 MD5 与 hashlib.md5 哈希结果不一样的情况,后来才发现,原来是我自己少取了2位哈希值(用了[2:])
    :return:
    """
    text = "ctf{345_manhattan_10282}"

    # hashlib
    md5 = hashlib.md5()
    md5.update(text.encode("utf8"))
    print(md5.hexdigest())

    # Crypto.Hash 中的 MD5
    print(MD5.new(text.encode("utf8")).hexdigest())


def main():
    flag = get_flag()
    print(flag)


if __name__ == "__main__":
    main()
