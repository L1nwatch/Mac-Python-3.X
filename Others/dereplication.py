#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: Mac 的照片库, 我在里面放了很多重复的照片, 但是一个个删除重复照片不太容易, 所以考虑用脚本解决
思路:
首先将照片库里所有照片都导出来, 然后放到同一个文件夹下, 我对这个文件夹的每一个文件都进行哈希处理, 然后去重复化
'''
__author__ = '__L1n__w@tch'

import os
import shutil
from Crypto.Hash import MD5


def dereplication(hash_dict):
    """
    思路是,对每一张图片进行遍历,通过哈希值判断是否已经放入了新的文件夹
    :param hash_dict:
    :return:
    """
    global old_path, new_path
    hash_set = set()
    for file_name, hash in hash_dict.items():
        if hash not in hash_set:
            shutil.copyfile(old_path + file_name, new_path + file_name)
            hash_set.add(hash)


def create_hash_dict(path):
    hash_dict = dict()
    for each_file in os.listdir(path):
        with open(path + each_file, "rb") as f:
            data = f.read()
            hash = MD5.new(data).digest()
            hash_dict[each_file] = hash
    return hash_dict


def main():
    global old_path, new_path
    new_path = "/Users/L1n/Desktop/new_tmp/"
    old_path = "/Users/L1n/Desktop/tmp/"
    hash_dict = create_hash_dict(old_path)
    dereplication(hash_dict)
    print("Done")


if __name__ == "__main__":
    main()
