#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.11 作为 utm 解析的单元测试文件
"""
import unittest
from utm_lib_parse import UTMParser

__author__ = '__L1n__w@tch'


class TestUTMParse(unittest.TestCase):
    def setUp(self):
        # TODO: 这里非得让我打用户名密码啥的?
        svn_info = ("https://200.200.0.8/svn/test/测试部文件服务器/测试工程/AF版本/AF规则/UTM规则验证/",
                    "linfeng", "lf123456", "./utm_urls_lib")
        self.utm_parser = UTMParser(svn_info)

    def test_extract_urls(self):
        """
        测试是否能够正确提取 url
        """
        test_file = "utm_url_test_file.txt"
        right_answer = {"seo-pronew.com/b/opt/DBC359C361E7BD8F63B8CF1A/", "twilight-duo.com/logo.gif",
                        "taiborucheng.com/b/opt/F1FA1A051C89D19CD7917D5C/", "wqmrierihon.com/index.php"}
        self.assertEqual(right_answer, self.utm_parser.extract_urls(test_file))


if __name__ == "__main__":
    pass
