#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 把所有子目录照片放到 root 目录下
"""
import os
import shutil


__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    root_path = r"/Users/L1n/Desktop/照片视频备份/深信服实习"
    dst_path = r"/Users/L1n/Desktop/照片视频备份/深信服实习"
    for root,dirs,files in os.walk(root_path):
        for each_file in files:
            shutil.move(os.path.join(root_path,root,each_file),os.path.join(dst_path,each_file))