#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://www.shiyanbar.com/ctf/717
密文xztiofwhf是用仿射函数y=5x+11加密得到的

这回居然百度百科解释得比较清楚:
    C= Ek(m)=(k1m+k2) mod n
    M= Dk(c)=k3(c- k2) mod n（其中（k3 ×k1）mod26 = 1）
'''
__author__ = '__L1n__w@tch'

import gmpy2
import string


def affine_decrypt(cipher_text, k1, k2, n):
    """
    按照 M= Dk(c)=k3(c- k2) mod n（其中（k3 ×k1）mod n = 1）进行解密操作
    :param cipher_text: "xztiofwhf"
    :param k1: 5
    :param k2: 11
    :return:
    """
    k3 = gmpy2.invert(k1, 26)
    plaintext = str()
    for each in cipher_text:
        plaintext += string.ascii_lowercase[k3 * (string.ascii_lowercase.find(each) - k2) % 26]

    return plaintext


def main():
    cipher_text = "xztiofwhf"
    k1 = 5
    k2 = 11
    n = 26
    plaintext = affine_decrypt(cipher_text, k1, k2, n)
    print(plaintext)


if __name__ == "__main__":
    main()
