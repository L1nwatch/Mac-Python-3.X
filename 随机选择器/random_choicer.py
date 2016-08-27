#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
20160827, 看电视困难症患者, 于是写个脚本, 随机从一堆列表中获取一个然后打开播放, 恩没其他功能了
"""
import os
import random

__author__ = '__L1n__w@tch'


def get_all_files_path_with_fix(root_path, files_fix):
    """
    获取指定目录下所有指定后缀的文件的路径, 返回一个列表
    :param root_path: "/Users/L1n/Desktop/Entertainment/进击的巨人第一季全集"
    :param files_fix: ["mp4", "mp3"]
    :return: ['/Users/L1n/Desktop/Entertainment/进击的巨人第一季全集/1.mp4', ...]
    """
    result_list = list()
    for root, dirs, files in os.walk(root_path):
        for each_file in files:
            for each_file_type in files_fix:
                if each_file.endswith(each_file_type):
                    result_list.append(root + os.sep + each_file)
                    break

    return result_list


def random_choice(choices):
    """
    实现随机选择
    :param choices: ["1", "2", "3"]
    :return: "3" or "2" or "1"
    """
    return random.choice(choices)


def open_a_file_with_right_app(file_path):
    """
    使用终端的 open 命令以默认 app 软件打开对应的文件, 注意由于终端需要路径转义, 这里需要手动替换对应字符
    :param file_path:  "/Users/L1n/Desktop/Entertainment/进击的巨人第一季全集/11.mp4"
    :return:
    """
    file_path = file_path.replace(r"[", r"\[")
    file_path = file_path.replace(r"]", r"\]")
    file_path = file_path.replace(r" ", r"\ ")
    os.system("open {}".format(file_path))


def random_choicer(root_path, file_types):
    a_list = get_all_files_path_with_fix(root_path, file_types)
    return random_choice(a_list)


def random_player(root_path, file_types):
    open_a_file_with_right_app(random_choicer(root_path, file_types))


if __name__ == "__main__":
    a_list = ["1", "2", "3"]
    result_set = set()

    for i in range(3):
        result_set.add(random.choice(a_list))

    print(result_set)
