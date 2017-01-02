#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.02 开始自动化测试模块
"""
try:
    import simplejson as json
except ImportError:
    import json

import requests
from pcap_scapy_parse import PcapParser

__author__ = '__L1n__w@tch'


class AutoTester:
    def __init__(self, result_json_file_path):
        """
        :param result_json_file_path: 解析 pcap 包得到的 json 格式文件
        """
        self.test_json_file = result_json_file_path

    def get_http_headers_list(self):
        """
        从 json 文件中读取每一个 http 头放到列表中
        :return: list(), 每一个元素是一个 http 头
        """
        with open(self.test_json_file, "r") as f:
            data_dict = json.load(f)

        result_list = list()

        for each_pcap, each_pcap_https in data_dict.items():
            for each_http in each_pcap_https:
                result_list.append(each_http)

        return result_list

    @staticmethod
    def parse_http_header(http_header):
        """
        解析 http 头, 拿到 url 以及 http 头其他参数
        :return: (url, http_header), 提供给 requests 作为封装使用
        """
        url = PcapParser.get_url_from_raw_data(http_header)
        http_parameter = dict()

        for each_parameter in str(http_header).split(r"\r\n"):
            item = each_parameter.split(":", 1)
            # 正常的 http 头字段
            if len(item) == 2:
                key, value = item[0], item[1]
                http_parameter[key] = value
            # 不是 http 头字段, 忽视
            else:
                continue

        return url, http_parameter

    def create_http_request(self, ip):
        """
        :param ip: 目标 IP, 构造请求时使用
        """
        # 提取每一个 HTTP 头
        http_header_list = self.get_http_headers_list()

        for each_http in http_header_list:
            # POST 请求
            if PcapParser.is_http_post_request_header(each_http):
                url, header = self.parse_http_header(each_http)
                response = requests.get("http://{}{}".format(ip, url), header=header)
                print(response.text)
                exit(0)

            # GET 请求
            elif PcapParser.is_http_get_request_header(each_http):
                url, header = self.parse_http_header(each_http)
                response = requests.get("http://{}{}".format(ip, url), headers=header)
                print(response.text)

                exit(0)
            else:
                raise RuntimeError("遇到无法解析的 HTTP 头了")

    def run(self, target_ip):
        """
        完成自动化测试流程
        :param target_ip: 测试服务器的 IP 地址
        """
        # 解析 HTTP 请求头, 按照 requests 库封装好并发送出去
        self.create_http_request(target_ip)


if __name__ == "__main__":
    at = AutoTester("2th_headers_result.json")
    at.run("192.168.114.2")
