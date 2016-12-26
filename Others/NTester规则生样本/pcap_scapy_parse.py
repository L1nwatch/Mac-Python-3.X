#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.26 尝试使用 scapy 库解析 pcap 包
"""
import scapy.all
import re
import os

__author__ = '__L1n__w@tch'


class PcapParser:
    @staticmethod
    def get_url_from_raw_data(data):
        """
        从 data 中提取 url
        :param data: b'GET /wordpress/wp-content/plugins/wpSS/ss_handler.php?display=0&edit=&ss_id=1%27%22 HTTP/1.1\r\nAccept: text/html, application/xhtml+xml, */*\r\nAccept-Language: zh-CN\r\nUser-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)\r\nAccept-Encoding: gzip, deflate\r\nHost: 192.168.41.68\r\nConnection: Keep-Alive\r\nCookie: acopendivids=swingset,phpbb2,redmine; acgroupswithpersist=nada; JSESSIONID=024D3D2EDA89A7BB595684F55788684A\r\n\r\n'
        :return: 'GET /wordpress/wp-content/plugins/wpSS/ss_handler.php?display=0&edit=&ss_id=1%27%22 HTTP/1.1'
        """
        result = re.findall("GET.*HTTP/1\.1", str(data))
        if len(result) == 1:
            return result[0]

    @staticmethod
    def get_raw_info(packet):
        """
        获取 raw 字段的内容
        :param packet: scapy 格式的数据包
        :return: raw 信息
        """
        return packet["TCP"]["Raw"]

    @staticmethod
    def is_http_packet(packet):
        """
        判断是否为 http 包, 需要完善内部细节
        :param packet: scapy 格式的包
        :return:
        """
        return "Raw" in packet["TCP"]

    def get_http_urls(self, pcap_file_path):
        """
        获取 pcap 中所有 HTTP 请求的 GET 或 POST 请求
        :param pcap_file_path: pcap 包路径
        :return: None
        """
        parse_data = scapy.all.utils.rdpcap(pcap_file_path)
        urls = list()

        for each_packet in parse_data:
            if self.is_http_packet(each_packet):
                url = self.get_url_from_raw_data(self.get_raw_info(each_packet))
                urls.append(url) if url else None
        return urls


if __name__ == "__main__":
    for each_pcap in os.listdir("waf"):
        file_path = "waf/{}".format(each_pcap)
        parser = PcapParser()
        urls = parser.get_http_urls(file_path)
        print("{} --> {}".format(file_path, urls))
