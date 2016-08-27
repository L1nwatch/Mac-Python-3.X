#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
对自己的内容搜索器进行编码方面的测试
"""
import unittest
from search_keyword import decode_content, search_keyword_infile, get_keyword

__author__ = '__L1n__w@tch'


class TestDecode(unittest.TestCase):
    def test_gbk(self):
        gbk_encode = "大家好".encode("gbk")
        self.assertEqual(decode_content(gbk_encode), "大家好")

    def test_utf8(self):
        utf8_encode = "呵呵哒".encode("utf8")
        self.assertEqual(decode_content(utf8_encode), "呵呵哒")

    @unittest.skip  # 工程不小心被我删除了...
    def test_search_gbk_comment(self):
        """
        测试是否能够搜索到 gbk 编码的注释
        :return:
        """
        test_path = "/Users/L1n/Desktop/Python Projects/PyCharm/文件内容搜索器/cacfg_src_v3.60.0010/PMDlgPersonCert.cpp"
        self.assertEqual(search_keyword_infile(test_path, "读存储"), '		AfxMessageBox("读存储设备出错!");')

    @unittest.skip  # 现在暂时不使用正则来匹配
    def test_get_keyword(self):
        """
        测试正则表达式是否能够正确匹配
        :return:
        """
        keyword = "keyword"
        # 测试情况1: 关键词位于第一行, 每一行以 \r\n 分隔
        content = "{} first line \r\nsecond \r\n".format(keyword)
        self.assertEqual(get_keyword(keyword, content), "{} first line \r\n".format(keyword))

        # 测试情况1: 关键词位于第一行, 每一行以 \n 分隔
        content = "{} first line \nsecond \n".format(keyword)
        self.assertEqual(get_keyword(keyword, content), "{} first line \n".format(keyword))

        # 测试情况2: 关键词位于最后一行, 每一行以 \r\n 分隔
        content = "first line \r\n{} second line\r\n".format(keyword)
        self.assertEqual(get_keyword(keyword, content), "{} second line\r\n".format(keyword))

        # 测试情况2: 关键词位于最后一行, 每一行以 \n 分隔
        content = "first line \n{} second line\n".format(keyword)
        self.assertEqual(get_keyword(keyword, content), "{} second line\n".format(keyword))

        # 测试情况3: 关键词位于中间某一行, 每一行以 \r\n 分隔
        content = "first line \r\n{} second line\r\nthird line\r\n".format(keyword)
        self.assertEqual(get_keyword(keyword, content), "{} second line\r\n".format(keyword))

        # 测试情况3: 关键词位于中间某一行, 每一行以 \n 分隔
        content = "first line \n{} second line\nthird line\n".format(keyword)
        self.assertEqual(get_keyword(keyword, content), "{} second line\n".format(keyword))

        # 测试情况4: 关键词不存在, 每一行以 \r\n 分隔
        content = "first line \r\nsecond line\r\nthird line\r\n"
        self.assertEqual(get_keyword(keyword, content), None)

        # 测试情况4: 关键词不存在, 每一行以 \n 分隔
        content = "first line \nsecond line\nthird line\n"
        self.assertEqual(get_keyword(keyword, content), None)

        # 测试情况5: 关键词存在于某一行的中间部分, 每一行以 \n 分隔
        content = "first line \nheiheiehei {}second line\nthird line\n".format(keyword)
        self.assertEqual(get_keyword(keyword, content), "heiheiehei {}second line\n".format(keyword))

        # 测试情况6: 关键词存在第一行, 且没有换行符
        content = "first {} line".format(keyword)
        self.assertEqual(get_keyword(keyword, content), "first {} line".format(keyword))


if __name__ == "__main__":
    pass
