#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 针对提取脚本作测试
"""
import unittest


__author__ = '__L1n__w@tch'

class TestExtract(unittest.TestCase):
    def test_extract_figure(self):
        """
        提取 figure 应该只提取 caption 字段
        :return:
        """
        pass

    def test_extract_segment(self):
        """
        能够自动提取代码段, 比如说 figure 代码段
        :return:
        """
        pass

    def test_extract_itemize(self):
        """
        验证提取 itemize 中的内容
        :return:
        """
        pass

    def test_extract_label(self):
        """
        针对 label 则不进行提取操作
        :return:
        """
        pass

if __name__ == "__main__":
    pass