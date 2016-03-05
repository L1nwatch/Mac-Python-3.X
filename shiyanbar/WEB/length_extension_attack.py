#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 原题: http://www.shiyanbar.com/ctf/1848
看了 WriteUp 之后知道得用哈希长度扩展攻击,于是下载 hashpumpy 研究一番
'''
__author__ = '__L1n__w@tch'

import hashpumpy


def main():
    hex_digest = "571580b26c65f306376d4f64e53cb5c7"
    original_data = "adminadmin"
    data_to_add = "aaaaa"
    key_length = 15

    md5, password = hashpumpy.hashpump(hex_digest, original_data, data_to_add, key_length)
    print("New Md5: {}, Original+Payload: {}".format(md5, password))


if __name__ == "__main__":
    main()
