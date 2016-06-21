#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 实现对指定文件夹下所有文件进行内容搜索, 关键词及搜索的文件类型由用户指定

2016.06.21 由于微机原理也要进行 ARM 平台小车的开发, 遇到了跟 ZigBee 一样的困境, 需要快速掌握工程文件, 所以还是将这个程序通用化吧
2016.04 起初编写这个程序是由于对协议栈不熟悉, 所以需要对协议栈的每一个文件进行关键词搜索, 同时列举出来
"""
import os
import argparse

__author__ = '__L1n__w@tch'


def is_valid_file_type(name, types):
    """

    :param name:
    :param types:
    :return:
    """
    for each_type in types:
        if name.endswith(each_type):
            return True
    return False


def add_argument(parser):
    """
    为解析器添加参数
    :param parser:
    :return:
    """
    parser.add_argument("--path", "-p", type=str,
                        default="/Users/L1n/Desktop/全国大学生信息安全竞赛/初赛/for_Python", help="文件夹路径")
    parser.add_argument("--type", "-t", type=str, default=".c#.h", help="搜索文件类型, 默认值及格式为: \".c#.h\"")
    parser.add_argument("--keyword", "-k", type=str, default="main", help="要搜索的关键词")


def set_argument(options):
    """
    读取用户输入的参数, 检验是否合法
    :param options: parser.opts
    :return: dict()
    """
    configuration = dict()
    configuration["path"] = options.path
    configuration["file_type"] = options.type.split("#")
    configuration["keyword"] = options.keyword.lower()

    print("[*] 要搜索的路径为: {}".format(configuration["path"]))
    print("[*] 要搜索的文件类型包括: {}".format(configuration["file_type"]))
    print("[*] 要搜索的关键词为: {}".format(configuration["keyword"]))

    return configuration


def initialize():
    parser = argparse.ArgumentParser(description="文件内容搜索程序")
    add_argument(parser)
    configuration = set_argument(parser.parse_args())

    print("[*] {} 搜索开始 {}".format("-" * 30, "-" * 30))

    return configuration["path"], configuration["file_type"], configuration["keyword"].encode("utf8")


if __name__ == "__main__":
    path, file_type, keyword = initialize()

    for root, dirs, files in os.walk(path):
        for each_file in files:
            if not is_valid_file_type(each_file, file_type):
                continue
            else:
                path = root + os.sep + each_file
                with open(root + os.sep + each_file, "rb") as f:
                    data = f.read().lower()
                    if keyword in data:
                        print("[*] Found in \"{}\", path is {}".format(each_file, path))
    print("[*] {} 搜索结束 {}".format("-" * 30, "-" * 30))
