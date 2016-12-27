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

        # 非 TCP 包
        packet = Ether() / IP() / UDP()
        self.assertFalse(self.pcap_parser.is_http_packet(packet))

    def test_filter_header(self):
        filter_list = ["favicon.ico"]
        test_header = "b'GET /favicon.ico HTTP/1.1\\r\\nHost: www.sangfor.com\\r\\nConnection: keep-alive\\r\\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36\\r\\nAccept: */*\\r\\nReferer: http://www.sangfor.com/wp-admin/admin.php?page=booking%2Fwpdev-booking.phpwpdev-booking&wh_approved&wh_is_new=1&wh_booking_date=3&view_mode=vm_listing\\r\\nAccept-Encoding: gzip, deflate, sdch\\r\\nAccept-Language: zh-CN,zh;q=0.8\\r\\nCookie: Hm_lvt_a3edfd653736089ca7c875a3ea4ebe59=1476155748; _ga=GA1.2.19483797.1471240472\\r\\n\\r\\n'"

        # 应该过滤为空
        self.assertEqual(self.pcap_parser.filter_header(test_header, filter_list), None)

    def test_has_point_info(self):
        pass

    def test_is_http_post_request_header(self):
        pass

    def test_is_http_get_request_header(self):
        pass


if __name__ == "__main__":
    pass
