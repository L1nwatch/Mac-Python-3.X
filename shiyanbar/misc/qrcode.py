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


def create_qrcode(tables, image_name):
    # 表格的列数得统一
    length = set([len(each) for each in tables])
    assert len(length) == 1
    length = length.pop()

    width, height = len(tables), length
    black, white = (0, 0, 0), (255, 255, 255)
    background_color = white
    image = Image.new("RGB", (width, height), background_color)
    pix = image.load()
    for x in range(width):
        for y in range(height):
            if chr(tables[x][y]) == "1":
                pix[x, y] = black
    image.save(image_name)


def main():
    with open("15AFFB.zlib", "rb") as f:
        data = f.read()
    data = zlib.decompress(data)
    tables = divide_group(data)

    qrcode_file_name = "qrcode.jpg"
    create_qrcode(tables, qrcode_file_name)


if __name__ == "__main__":
    main()
