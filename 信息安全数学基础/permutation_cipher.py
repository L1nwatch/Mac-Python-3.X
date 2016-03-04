#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 学信息安全数学基础课程,结果老师居然布置了一道加密题,习惯性地用 Python 来写了
题目描述如下:
    用密码 1->2 2->4 3->1 4->3 加密字符串"HELLO WORLD!"

思路:
    每 4 个一组,然后第2个字符放到第一个,第4个字符放到第2个,以此类推
'''
__author__ = '__L1n__w@tch'

from itertools import zip_longest


def permutation_encrypt(plain_text):
    """
    置换方式: 1->2 2->4 3->1 4->3
    :param plain_text: "HELLO WORLD!"
    :return:
    """
    answer = str()
    blocks = divide_group(bytes(plain_text, "utf-8"), 4)
    for block in blocks:
        block = [block[1], block[3], block[0], block[2]]
        answer += str().join([chr(char) for char in block])
    return answer


def divide_group(text, size=16):
    """
    :param text: b"12345678"
    :param size: 3
    :return: [b"123", b"456", b"78"]
    """
    args = [iter(text)] * size
    blocks = list()
    for block in zip_longest(*args):
        blocks.append(b"".join([bytes([value]) for value in block if value is not None]))

    return blocks


def main():
    plain_text = "HELLO WORLD!"
    cipher_text = permutation_encrypt(plain_text)
    print(cipher_text)


if __name__ == "__main__":
    main()
