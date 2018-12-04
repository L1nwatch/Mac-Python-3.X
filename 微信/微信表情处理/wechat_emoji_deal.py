#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 微信表情包重命名等处理
"""
import os
import datetime
import shutil
from collections import Counter

__author__ = '__L1n__w@tch'


def rename():
    """
    把所有表情都重命名一遍
    :return:
    """
    src_path = "wechat_emoji"
    dst_path = "after_rename_emoji"
    os.makedirs(dst_path, exist_ok=True)

    for each_file in os.listdir(src_path):
        if "DS_Store" in each_file:
            os.remove(os.path.join(src_path, each_file))
            continue
        os.rename(os.path.join(src_path, each_file), os.path.join(src_path, "{}.gif".format(each_file)))
        # shutil.copy(os.path.join(src_path, "{}.gif".format(each_file)),
        #             os.path.join(dst_path, "{}.gif".format(each_file)))


def split_using_time():
    """
    根据修改时间来分类表情包
    :return:
    """
    src_path = "wechat_emoji"

    emoji_set = set()

    for each_file in os.listdir(src_path):
        emoji_type = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(src_path, each_file)))
        emoji_type = str(emoji_type)
        if emoji_type not in emoji_set:
            emoji_set.add(emoji_type)
            os.makedirs(os.path.join("temp_result", emoji_type), exist_ok=True)
        shutil.copy(os.path.join(src_path, each_file), os.path.join("temp_result", emoji_type, each_file))


def extract_packet_using_num():
    """
    根据每个文件夹的文件个数,提取
    :return:
    """
    root_path = "temp_result"
    dst_path = "result"
    count_result = dict()
    for each_dir in os.listdir(root_path):
        if "DS_Store" in each_dir:
            continue
        num = len(os.listdir(os.path.join(root_path, each_dir)))
        print("[*] {}:{}".format(each_dir, num))
        count_result[each_dir] = num
    for i, (key, value) in enumerate(count_result.items()):
        if value > 2:
            shutil.copytree(os.path.join(root_path, key), os.path.join(dst_path, str(i)))


def rename_each_file():
    """
    把最终结果中每个文件都重命名一下
    :return:
    """
    count = 0
    root_path = "result"
    for each_dir in os.listdir(root_path):
        if os.path.isfile(each_dir):
            continue
        for each_file in os.listdir(os.path.join(root_path, each_dir)):
            os.rename(os.path.join(root_path, each_dir, each_file),
                      os.path.join(root_path, each_dir, "{}.gif".format(count)))
            count += 1


def finally_rename():
    """
    最后对表情包进行重命名
    :return:
    """
    root_path = r"/Users/L1n/Desktop/result/双拼乖巧_低清"
    dst_path = r"/Users/L1n/Desktop/result/双拼乖巧_低清_result"
    os.makedirs(dst_path, exist_ok=True)

    base_num = 192  # 2018-09-09 乖巧小人总共有 xx 个
    # base_num = 345  # 2018-09-09 嗷大喵总共有 xx 个
    # base_num = 360  # 2018-09-09 长草颜丸子总共有 xx 个

    for i, each_file in enumerate(os.listdir(root_path)):
        if "DS_Store" in each_file:
            base_num -= 1
            continue
        file_name, ext = os.path.splitext(each_file)
        shutil.copy(os.path.join(root_path, each_file), os.path.join(dst_path, "{}{}".format(i + base_num + 1, ext)))
        # for i, each_file in enumerate(os.listdir(root_path)):
        #     if "DS_Store" in each_file:
        #         continue
        #     os.rename(os.path.join(root_path, each_file), os.path.join(root_path, "{}.gif".format(i)))


if __name__ == "__main__":
    rename()
    split_using_time()
    extract_packet_using_num()
    rename_each_file()
    # finally_rename()
