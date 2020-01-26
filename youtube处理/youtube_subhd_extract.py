#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" youtube 字幕提取
"""
import re

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    with open("字幕.txt", encoding="utf8") as f:
        data = f.read()
        result = re.findall('<div class="cue style-scope[^>]*?>([\s\S]+?)</div>', data)
        for each_result in result:
            print(each_result.strip())
