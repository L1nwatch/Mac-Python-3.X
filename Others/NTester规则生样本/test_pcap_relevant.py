#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.26 作为 pcap 包相关测试文件
"""
import unittest
import os
from scapy.all import *
from pcap_scapy_parse import PcapParser

__author__ = '__L1n__w@tch'


class TestPcapParser(unittest.TestCase):
    def setUp(self):
        self.pcap_parser = PcapParser()

    def test_get_url_from_raw_data(self):
        """
        给定 raw_data 看是否能够正确获取 url 对应的那一条信息
        :return:
        """
        test_input = b'GET /wordpress/wp-content/plugins/wpSS/ss_handler.php?display=0&edit=&ss_id=1%27%22 HTTP/1.1\r\nAccept: text/html, application/xhtml+xml, */*\r\nAccept-Language: zh-CN\r\nUser-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)\r\nAccept-Encoding: gzip, deflate\r\nHost: 192.168.41.68\r\nConnection: Keep-Alive\r\nCookie: acopendivids=swingset,phpbb2,redmine; acgroupswithpersist=nada; JSESSIONID=024D3D2EDA89A7BB595684F55788684A\r\n\r\n'
        right_answer = 'GET /wordpress/wp-content/plugins/wpSS/ss_handler.php?display=0&edit=&ss_id=1%27%22 HTTP/1.1'
        my_answer = self.pcap_parser.get_url_from_raw_data(test_input)
        self.assertEqual(my_answer, right_answer)

    def test_get_raw_info(self):
        """
        测试是否能够正确从一个 packet 包中获取 raw 信息
        :return:
        """
        random_raw_data = os.urandom(8)
        test_packet = Ether() / IP() / TCP() / Raw(random_raw_data)
        my_answer = self.pcap_parser.get_raw_info(test_packet)
        self.assertEqual(my_answer, Raw(random_raw_data))

    def test_is_http_packet(self):
        """
        测试判断是否为 http 包的这个方法是否对的, 目前是基于 Raw 进行判断的
        :return:
        """
        # 非 Raw 包
        packet = Ether() / IP() / TCP()
        self.assertFalse(self.pcap_parser.is_http_packet(packet))

        # Raw 包
        packet /= Raw(b"test")
        self.assertTrue(self.pcap_parser.is_http_packet(packet))


if __name__ == "__main__":
    pass
