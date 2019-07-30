#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    pass

import os

root_path = unicode(r"/Users/L1n/Desktop/长草颜团子X旱瀬")
dst_root_path = unicode(r"/Users/L1n/Desktop/长草颜团子X旱瀬-微信")

for root, dirs, files in os.walk(root_path):
    for each_file in files:
        if each_file == ".DS_Store":
            continue
        src_file_path = os.path.join(root, each_file)
        image = pdb.file_gif_load(src_file_path, "test")
        dst_file_path = os.path.join(dst_root_path, root[len(root_path) + 1:])
        if not os.path.exists(dst_file_path):
            os.makedirs(dst_file_path)
        dst_file_path = os.path.join(dst_file_path, each_file)
        pdb.file_gif_save(image, None, dst_file_path, dst_file_path, 1, 1, 100, 2)