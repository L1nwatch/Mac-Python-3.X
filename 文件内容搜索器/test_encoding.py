#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
对自己的内容搜索器进行编码方面的测试
"""
import unittest
from search_keyword import decode_content

__author__ = '__L1n__w@tch'


class TestDecode(unittest.TestCase):
    def test_gbk(self):
        gbk_encode = "大家好".encode("gbk")
        self.assertEqual(decode_content(gbk_encode), "大家好")

    def test_utf8(self):
        utf8_encode = "呵呵哒".encode("utf8")
        self.assertEqual(decode_content(utf8_encode), "大家好")


if __name__ == "__main__":
    pass
