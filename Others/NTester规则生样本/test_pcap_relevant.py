#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.26 作为 pcap 包相关测试文件
"""
import unittest
import codecs
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
        right_answer = b'/wordpress/wp-content/plugins/wpSS/ss_handler.php?display=0&edit=&ss_id=1%27%22'
        my_answer = self.pcap_parser.get_url_from_raw_data(test_input)
        self.assertEqual(my_answer, right_answer)

        test_input = b"GET /dvwa/vulnerabilities/c99shell.php HTTP/1.0\r\nAccept: */*\r\nUser-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322)\r\nHost: 192.168.41.68\r\nCookie: PHPSESSID=812tfnicu1dt2lu9u5btnkjm92;security=low\r\nConnection: Close\r\nPragma: no-cache\r\nAcunetix-Product: WVS/5.1 (Acunetix Web Vulnerability Scanner - NORMAL)\r\nAcunetix-Scanning-agreement: Third Party Scanning PROHIBITED\r\nAcunetix-User-agreement: http://www.acunetix.com/wvs/disc.htm\r\n\r\n"
        right_answer = b'/dvwa/vulnerabilities/c99shell.php'
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
        """
        测试是否能过正确过滤包含指定资源的头部
        """
        filter_list = ["ico", "jpg", "gif", "js", "css"]
        test_headers = [
            b"GET /favicon.ico HTTP/1.1\r\n",
            b"GET /new/bg.jpg HTTP/1.1\r\n",
            b"GET /new/images/index_r3_c4.gif HTTP/1.1\r\n",
            b"get /new/js/search.js HTTP/1.1\r\n",
            b"GET /new/sty.css HTTP/1.1\r\n"]

        # 应该过滤为空
        for each_header in test_headers:
            self.assertEqual(self.pcap_parser.filter_header(each_header, filter_list), None)

        test_header = b"GET / HTTP/1.1\r\n"
        self.assertEqual(self.pcap_parser.filter_header(test_header, filter_list), b"GET / HTTP/1.1\r\n")

    def test_has_point_info(self):
        """
        测试是否能够判断准确, 这里只判断 /favicon.ico 这一个资源, 然后判断 POST 和 GET 请求
        """
        filter_list = ["ico"]

        # GET 包含这个资源
        self.assertTrue(self.pcap_parser.has_point_info(b"GET /favicon.ico HTTP/1.1", filter_list))

        # GET 不包含这个资源
        self.assertFalse(self.pcap_parser.has_point_info(b"GET /favicon.ic HTTP/1.1", filter_list))

        # POST 包含这个资源
        self.assertTrue(self.pcap_parser.has_point_info(b"POST /favicon.ico HTTP/1.1", filter_list))

        # POST 不包含这个资源
        self.assertFalse(self.pcap_parser.has_point_info(b"POST /favicon.io HTTP/1.1", filter_list))

    def test_is_http_post_request_header(self):
        """
        测试判断 POST 请求头是否正确
        """
        # POST 请求
        self.assertTrue(self.pcap_parser.is_http_post_request_header(b"POST /favicon.ico HTTP/1.1"))

        # POST 请求2
        self.assertTrue(self.pcap_parser.is_http_post_request_header(b"PoST /favicon.ico HTTP/1.1"))

        # 非 POST 请求
        self.assertFalse(self.pcap_parser.is_http_post_request_header(b"POS /favicon.ico HTTP/1.1"))

        # 非 POST 请求2
        self.assertFalse(self.pcap_parser.is_http_post_request_header(b"POSTPOST /favicon.ico HTTP/1.1"))

    def test_is_http_get_request_header(self):
        """
        测试判断 GET 请求头是否正确
        """
        # GET 请求
        self.assertTrue(self.pcap_parser.is_http_get_request_header(b"GET /favicon.ico HTTP/1.1"))

        # GET 请求 2
        self.assertTrue(self.pcap_parser.is_http_get_request_header(b"gET /favicon.ico HTTP/1.1"))

        # 非 GET 请求
        self.assertFalse(self.pcap_parser.is_http_get_request_header(b"GETS /favicon.ico HTTP/1.1"))

        # 非 GET 请求 2
        self.assertFalse(self.pcap_parser.is_http_get_request_header(b"GETGET /favicon.ico HTTP/1.1"))

        # GET 请求 3
        test_data = b"GET /detail.php?id=1%20and%20'a'&'a' HTTP/1.1\r\nHost: www.shenxinfu.com\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: gzip,deflate,sdch\r\nAccept-Language: zh-CN,zh;q=0.8\r\nAccept-Charset: GBK,utf-8;q=0.7,*;q=0.3"
        self.assertTrue(self.pcap_parser.is_http_get_request_header(test_data))

    def test_is_pcap_file(self):
        """
        测试 pcap 包是否判断准确
        """
        # 只出现一次 pcap, 且为后缀
        self.assertTrue(self.pcap_parser.is_pcap_file("waf/102323.pcap"))

        # 一次 pcap, 非后缀
        self.assertFalse(self.pcap_parser.is_pcap_file("pcap.pacps"))

        # 多次 pcap, 后缀
        self.assertTrue(self.pcap_parser.is_pcap_file("pcAp.pcaps.pcap"))

        # 多次 pcap, 非后缀
        self.assertFalse(self.pcap_parser.is_pcap_file("pcAp.pscpas.pcap.sss"))

        # 大小写
        self.assertTrue(self.pcap_parser.is_pcap_file("tet..pCap"))


if __name__ == "__main__":
    pass
