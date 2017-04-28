#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 自己写的论文是 LaTex 格式, 论文查重需要文本内容, 所以还是写个脚本来提取好了

2017.04.28 开始针对初始脚本进行提取
"""
import os

__author__ = '__L1n__w@tch'


class LatexExtract:
    def run(self, source_file_path):
        for each_file in (x for x in os.listdir(source_file_path) if x.endswith(".tex") and x.startswith("chap-")):
            print(each_file)


if __name__ == "__main__":
    source_file_dir = "source_file"

    le = LatexExtract()
    le.run(source_file_dir)
