#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.10 加入了解压 gz/tar 文件的方法, 优化了各种交互信息
2017.01.10 加入了提取 HTTP 请求失败时的情况处理
2017.01.09 优化好了 pcap 包解析, 现在可以解析不止 waf 路径了, 但是还存在 bug
2017.01.02 加入 json 模块, 用于封装中间数据
2016.12.27 导师说不要获取 URL 了, 而是直接拿下整个 http 头
2016.12.26 尝试使用 scapy 库解析 pcap 包
"""
# TODO: 不支持没有 HTTP 请求的 pcap 包, 比如 SMTP 协议, 纯 TCP 协议, 可以考虑写个方法把这些包复制出来, 方便以后研究

import gzip
import tarfile
import scapy.all
import re
import os
from scapy.error import Scapy_Exception

try:
    import simplejson as json
except ImportError:
    import json

__author__ = '__L1n__w@tch'


class PcapParser:
    @staticmethod
    def get_url_from_raw_data(data):
        """
        从 data 中提取 url
        :param data: b'GET /wordpress/wp-content/plugins/wpSS/ss_handler.php?display=0&edit=&ss_id=1%27%22 HTTP/1.1\r\nAccept: text/html, application/xhtml+xml, */*\r\nAccept-Language: zh-CN\r\nUser-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)\r\nAccept-Encoding: gzip, deflate\r\nHost: 192.168.41.68\r\nConnection: Keep-Alive\r\nCookie: acopendivids=swingset,phpbb2,redmine; acgroupswithpersist=nada; JSESSIONID=024D3D2EDA89A7BB595684F55788684A\r\n\r\n'
        :return: 'GET /wordpress/wp-content/plugins/wpSS/ss_handler.php?display=0&edit=&ss_id=1%27%22 HTTP/1.1'
        """
        result = re.findall("[GETPOST]{3,4} (.*) HTTP/1\.[01]", str(data), flags=re.IGNORECASE)
        if len(result) == 1:
            return result[0]

    @staticmethod
    def get_raw_info(packet):
        """
        获取 raw 字段的内容
        :param packet: scapy 格式的数据包
        :return: raw 信息, Raw() 格式
        """
        return packet["TCP"]["Raw"]

    @staticmethod
    def is_http_packet(packet):
        """
        判断是否为 http 包, 需要完善内部细节
        :param packet: scapy 格式的包
        :return: True or False
        """
        if "TCP" in packet and "Raw" in packet["TCP"]:
            return True
        return False

    def get_http_urls(self, pcap_file_path):
        """
        获取 pcap 中所有 HTTP 请求的 GET 或 POST 请求
        :param pcap_file_path: pcap 包路径
        :return: list(), 保存所有 pcap 包及其 url 的映射结果
        """
        parse_data = scapy.all.utils.rdpcap(pcap_file_path)
        urls = list()

        for each_packet in parse_data:
            if self.is_http_packet(each_packet):
                url = self.get_url_from_raw_data(self.get_raw_info(each_packet))
                urls.append(url) if url else None
        return urls

    @staticmethod
    def is_http_get_request_header(data):
        """
        判断是不是 GET 请求的 http 头
        :return: True or False
        """
        result = re.findall("^GET .*HTTP/1\.[01]", str(data), flags=re.IGNORECASE)
        return len(result) == 1

    @staticmethod
    def is_http_post_request_header(data):
        """
        判断是不是 POST 请求的 http 头
        :return: True or False
        """
        result = re.findall("^POST .*HTTP/1\.[01]", str(data), flags=re.IGNORECASE)
        return len(result) == 1

    @staticmethod
    def has_point_info(header, filter_list):
        """
        判断一个包里是否请求了指定的资源, 比如说请求了 favico.ico 资源
        :param header: str(), 包头
        :param filter_list: list(), 指定资源列表
        :return: True or False, 表示包含时返回 True
        """
        request_file = str(re.findall("[GETPOST]{3,4} (.*) HTTP/1\.[10]", header, flags=re.IGNORECASE)[0])

        for each_filter in filter_list:
            if request_file.endswith(each_filter):
                return True
        return False

    def filter_header(self, http_header, filter_list=None):
        """
        过滤掉没必要的头部, 比如说 GET /favicon.ico HTTP/1.1\r\n 这一类的
        :param http_header: 待过滤的头部列表
        :param filter_list: 要过滤的类型, 比如 ["ico"]
        :return: 过滤后的头部, 可能为 None, 也可能保持原状
        """
        result_header = None
        # 设置过滤的默认列表, TODO: 这个过滤默认列表是不是可以提取出来
        filter_list = ["ico", "jpg", "gif", "js", "css", "png"] if not filter_list else filter_list

        if self.is_http_get_request_header(http_header) or self.is_http_post_request_header(http_header):
            if not self.has_point_info(http_header, filter_list):
                result_header = http_header

        return result_header

    def get_http_headers(self, pcap_file_path):
        """
        获取 pcap 中所有 HTTP 请求的头部信息
        :param pcap_file_path: pcap 包路径
        :return: list(), 保存所有 pcap 包及其 header 的映射结果
        """
        headers = list()

        try:
            parse_data = scapy.all.utils.rdpcap(pcap_file_path)
            for each_packet in parse_data:
                if self.is_http_packet(each_packet):
                    header = str(self.get_raw_info(each_packet)).strip("b'\"")  # 去掉表示 byte 的符号
                    header = header.replace(r"\r\n", "\r\n")  # 去掉多余转义符号
                    # 过滤一下
                    header = self.filter_header(header)
                    headers.append(header) if header else None  # 如果过滤完不为空就添加
        except Scapy_Exception:
            print("[!] 解析: {} 失败".format(pcap_file_path))
        finally:
            return list(set(headers))  # 去掉重复的请求头

    @staticmethod
    def is_pcap_file(file_path):
        """
        判断是不是 pcap 包, 目前只是通过简单的判断后缀名来确定
        :param file_path: pcap 包路径
        :return: True or False
        """
        return file_path.lower().endswith(".pcap")

    def get_all_pcaps(self, pcaps_path):
        """
        递归遍历指定目录下所有文件, 读取 pcap 包路径出来
        :param pcaps_path: pcaps 包根目录
        :return: iterator, 包括了每一个 pcap 包路径
        """
        for root, dirs, files in os.walk(pcaps_path):
            for each_file in files:
                file_path = root + os.sep + each_file
                if self.is_pcap_file(file_path):
                    yield file_path

    def decompress_all_files(self, root_path):
        """
        解压指定目录下所有 gz 和 tar 包
        :param root_path:  str(), 根目录
        """
        self.print_message("开始解压 gz 包")
        for each_gz in os.listdir(root_path):
            if each_gz.endswith(".gz"):
                self.un_gz(os.path.join(root_path, each_gz))
        self.print_message("解压 gz 包完毕")

        self.print_message("开始解压 tar 包")
        for each_tar in os.listdir(root_path):
            if each_tar.endswith(".tar"):
                self.un_tar(os.path.join(root_path, each_tar))
        self.print_message("解压 tar 包完毕")

    def run(self, result_file_path, pcaps_root_path):
        """
        完成从读取 pcap 包到提取结果写入 json 文件
        :param result_file_path: str(), 目标 json 文件路径
        :param pcaps_root_path: str(), pcap 包压缩文件所在的根目录, 假设压缩格式为 gz
        """
        # 解压所有 gz/tar 格式的压缩文件, TODO: 注意只解压一级目录
        self.decompress_all_files(pcaps_root_path)

        # 开始解析所有 pcap 包
        self.print_message("开始提取目录 {} 下所有 pcap 包的 HTTP 请求".format(pcaps_root_path))
        with open(result_file_path, "w") as f:
            data_dict = dict()

            all_pcap_file = self.get_all_pcaps(pcaps_root_path)
            for each_pcap in all_pcap_file:
                urls = self.get_http_headers(each_pcap)
                if urls is False or len(urls) == 0:
                    print("[!] 提取 {} HTTP 请求失败".format(each_pcap))
                else:
                    data_dict[each_pcap] = urls

            json.dump(data_dict, f)

    @staticmethod
    def print_message(message):
        """
        格式化打印信息
        :param message: 要打印的信息
        """
        print("[*] {sep} {message} {sep}".format(sep="=" * 30, message=message))

    @staticmethod
    def un_gz(file_path):
        """
        解压 gz 文件, 假设 gz 文件里面只有一个 tar 文件
        :param file_path: str(), gz 文件路径
        :return: str(), 从 gz 提取出来的那个文件的文件路径
        """
        PcapParser.print_message("开始解压 gz 文件: {}".format(file_path))

        g_file = gzip.GzipFile(file_path)
        un_gz_file_path = os.path.splitext(file_path)[0]
        with open(un_gz_file_path, "wb") as f:
            f.write(g_file.read())

        PcapParser.print_message("解压完毕")

        return un_gz_file_path

    @staticmethod
    def un_tar(file_path):
        """
        解压 tar 文件, 假设 tar 文件里有多个文件
        :param file_path: tar 文件路径
        :return: str(), 解压后文件的根目录
        """
        with tarfile.open(file_path) as tar:
            file_names = tar.getnames()
            dir_path = os.path.splitext(file_path)[0]

            # 如果目录不存在则创建
            if not os.path.isdir(dir_path):
                os.mkdir(dir_path)

            # 提取每一个文件
            for each_file in file_names:
                each_file_path = os.path.join(dir_path, each_file)
                if os.path.exists(each_file_path):
                    print("[!] 解压文件 {} 已存在".format(each_file_path))
                else:
                    tar.extract(each_file, dir_path + os.sep)

        return dir_path


if __name__ == "__main__":
    parser = PcapParser()
    parser.run("2th_headers_result.json", "full_test")
