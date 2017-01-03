#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.03 提供了一个可以生成十六进制流的方法了
2017.01.03 这个模块负责与 NTester 交互生成所需的 lib 文件的
"""
import binascii
from itertools import zip_longest

__author__ = '__L1n__w@tch'


def create_hex_stream(data):
    """
    将给定的 data 转化为指定格式的十六进制流
    :param data: "GET /wp-content/plugins/ajax-store-locator-wordpress/sl_file_download.php?download_file=../../passwd HTTP/1.1\r\nHost: www.nationwidemri.com\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36\r\nAccept-Encoding: gzip, deflate, sdch\r\nAccept-Language: zh-CN,zh;q=0.8,en;q=0.6\r\n\r\n"
    :return: str(), "47 45 54 20 2f..."
    """
    hex_data = binascii.hexlify(data.encode("utf8"))
    hex_data = str(hex_data).strip("b'")
    return " ".join(divide_group(hex_data, 2))


def divide_group(text, size):
    """
    分组函数
    :param text: 待分组的内容, 474554202f7770
    :param size: 分组长度, 2
    :return: ['47', '45', '54', '20', '2f', '77', '70']
    """
    args = [iter(text)] * size
    blocks = list()
    for block in zip_longest(*args):
        blocks.append("".join(block))

    return blocks


if __name__ == "__main__":
    test_data = "GET /wp-content/plugins/ajax-store-locator-wordpress/sl_file_download.php?download_file=../../passwd HTTP/1.1\r\nHost: www.nationwidemri.com\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36\r\nAccept-Encoding: gzip, deflate, sdch\r\nAccept-Language: zh-CN,zh;q=0.8,en;q=0.6\r\n\r\n"
    create_hex_stream(test_data)
