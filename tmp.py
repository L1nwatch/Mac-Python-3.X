#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 现在才知道 zlib 原来是个可以解压的东西,怪不得我直接打开文本还是查看 16 进制都没有办法得到 wp 的那堆 01 串
'''
__author__ = '__L1n__w@tch'

import zlib
from itertools import zip_longest
from PIL import Image


def divide_group(data, block_size=25):
    """
    :param data: b"abcdefghi"
    :block_size: 3
    :return: [b"abc", b"def", b"ghi"]
    """
    args = [iter(data)] * block_size

    blocks = []
    for block in zip_longest(*args):
        blocks.append(b"".join([bytes([value]) for value in block]))

    return blocks


def main():
    text = b"01110011111110111111101001010000111010101110010111111011000111001000110111111111111110011010100111101011011110001100000110011110"
    print(hex(int(text, 2)))
    print(len("0x73fbfa50eae5fb1c8dfff9a9eb78c19e"))
    print("73fbfa50eae5fb1c8dfff9a9eb78c19e".upper())


if __name__ == "__main__":
    main()
