#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 由于对协议栈不熟悉, 所以需要对协议栈的每一个文件进行关键词搜索, 同时列举出来
'''
__author__ = '__L1n__w@tch'

import os


def is_valid_file_type(name, type):
    """

    :param name:
    :param type:
    :return:
    """
    for each_type in type:
        if name.endswith(each_type):
            return True
    return False


def configurate():
    configuration = dict()

    configuration["path"] = "/Users/L1n/Desktop/全国大学生信息安全竞赛/for_Python"
    configuration["file_type"] = [".c", ".h"]

    print("[*] Only search keyword in filetype: {}".format(configuration["file_type"]))
    configuration["keyword"] = input("[!] Input keyword: ").encode("utf8").lower()
    print("[*] Search keyword:{}".format(configuration["keyword"].decode("utf8")))
    print("[*] {} Search Begin {}".format("-" * 30, "-" * 30))

    return configuration


if __name__ == "__main__":
    configuration = configurate()

    for root, dirs, files in os.walk(configuration["path"]):
        for each_file in files:
            if not is_valid_file_type(each_file, configuration["file_type"]):
                continue
            else:
                path = root + os.sep + each_file
                with open(root + os.sep + each_file, "rb") as f:
                    data = f.read().lower()
                    if configuration["keyword"] in data:
                        print("[*] Found in \"{}\", path is {}".format(each_file, path))
    print("[*] {} Search End {}".format("-" * 30, "-" * 30))
