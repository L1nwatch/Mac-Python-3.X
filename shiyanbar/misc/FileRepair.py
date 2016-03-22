#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://www.shiyanbar.com/ctf/42
题目描述:
看格式这个图片是GIF的
解题链接： http://ctf5.shiyanbar.com:8080/stega/gif.gif

看了 wp 之后知道是文件头缺失,但是我并没有找到有用的工具能来帮我修复文件头的,所以我考虑自己手写一个
参考的文件头列表: http://blog.csdn.net/guoguo1980/article/details/5317665
'''
__author__ = '__L1n__w@tch'

import binascii

header_dict = {
    "jpg": "FFD8FF",
    "png": "89504E47",
    "gif": "47494638",
    "tif": "49492A00",
    "bmp": "424D"  # TODO: 还有很多文件头没收录,参考开头注释中的文件头列表
}


class FileRepair:
    # TODO: 后续还可以添加个函数,比如说有一部分文件头已经存在于头部了,这时只要补充下缺失的部分字节即可
    @staticmethod
    def add_header(file_name, type):
        """
        往一个文件添加指定类型的文件头
        :param file_name: str()
        :param type: "gif"
        :return: "fixed_{file_name}.{type}"
        """
        with open(file_name, "rb") as f:
            data = f.read()
        new_file_name = "fixed_" + file_name
        with open(new_file_name, "wb") as f:
            f.write(binascii.unhexlify(header_dict[type]))
            f.write(data)
        return new_file_name


def main():
    FileRepair.add_header("test.gif", "gif")


if __name__ == "__main__":
    main()
