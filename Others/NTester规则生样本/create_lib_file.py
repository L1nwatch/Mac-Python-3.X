#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.09 完善整个格式化流程
2017.01.03 提供了一个可以生成十六进制流的方法了
2017.01.03 这个模块负责与 NTester 交互生成所需的 lib 文件的
"""
try:
    import simplejson as json
except ImportError:
    import json

import binascii
import base64
import math
import re
import sqlite3
from Crypto.Cipher import DES
from itertools import zip_longest
from auto_test_module import AutoTester
from collections import namedtuple

__author__ = '__L1n__w@tch'


class LibCreator:
    def __init__(self, key, iv, result_json_file_path):
        """
        :param result_json_file_path: 解析 pcap 包得到的 json 格式文件
        :param key: des 密钥
        :param iv: des-CBC 模式使用的 iv
        """
        self.key = key
        self.iv = iv
        self.test_json_file = result_json_file_path

    @staticmethod
    def padding(data, size=8):
        """
        进行 PKCS#5 填充
        :param data: 待填充的数据, b"YELLOW SUBMARINE"
        :param size: 整数倍数, 比如说 8, 即表示填充到 8 的整数倍
        :return: 填充后的数据, b"YELLOW SUBMARINE\x08\x08\x08\x08\x08\x08\x08\x08"
        """
        pad_value = size - len(data) % size
        return data + bytes([pad_value]) * pad_value

    @staticmethod
    def un_padding(data, size=8):
        """
        进行 PKCS#5 解填充操作
        :param data: b"ICE ICE BABY\x04\x04\x04\x04"
        :param size: 块的长度, 比如 16
        :return: b"ICE ICE BABY"
        """
        # 抛出异常也可以用assert
        assert (len(data) % size == 0)
        padding_value = data[-1]
        # 以下的 -1 注意不要写成 padding_text[-padding_value:-1], 这样导致少了一个字节
        assert (data[-padding_value:] == bytes([padding_value]) * padding_value)
        return data[:len(data) - padding_value]

    def des_encrypt(self, plain_text):
        """
        进行 DES 加密, 模式固定为 CBC, 密钥由初始化决定, 最终输出结果经过 base64 编码
        :param plain_text: byte(), 明文数据, b"a" * 16
        :return: byte(), 加密过后的数据, b'AbY8o47jFJtuQRNbaAEqtTHRhd/h+RS5'
        """
        des = DES.new(self.key, DES.MODE_CBC, IV=self.iv)
        cipher_text = des.encrypt(self.padding(plain_text))
        base64_cipher_text = base64.b64encode(cipher_text)
        return base64_cipher_text

    def des_decrypt(self, plain_text):
        """
        进行 DES 加密, 模式固定为 CBC, 密钥由初始化决定
        :param plain_text: byte(), 待解密密文, b'AbY8o47jFJtuQRNbaAEqtTHRhd/h+RS5'
        :return: byte(), 解密后结果, b"a" * 16
        """
        des = DES.new(self.key, DES.MODE_CBC, IV=self.iv)
        unbase64_cipher_text = base64.b64decode(plain_text)
        plain_text = des.decrypt(unbase64_cipher_text)
        return self.un_padding(plain_text)

    def create_hex_stream(self, data):
        """
        将给定的 data 转化为指定格式的十六进制流
        :param data: "GET /wp-content/plugins/ajax-store-locator-wordpress/sl_file_download.php?download_file=../../passwd HTTP/1.1\r\nHost: www.nationwidemri.com\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36\r\nAccept-Encoding: gzip, deflate, sdch\r\nAccept-Language: zh-CN,zh;q=0.8,en;q=0.6\r\n\r\n"
        :return: str(), "47 45 54 20 2f..."
        """
        hex_data = binascii.hexlify(data.encode("utf8"))
        hex_data = str(hex_data).strip("b'\"")
        hex_data = hex_data.zfill(math.ceil(len(hex_data) / 2) * 2)
        return " ".join(self.divide_group(hex_data, 2))

    @staticmethod
    def divide_group(text, size):
        """
        分组函数
        :param text: 待分组的内容, str(), "474554202f7770"
        :param size: 分组长度, 2
        :return: ['47', '45', '54', '20', '2f', '77', '70']
        """
        assert len(text) % size == 0
        args = [iter(text)] * size
        blocks = list()
        for block in zip_longest(*args):
            blocks.append("".join(block))

        return blocks

    def format_json_file_to_hex_stream(self):
        """
        将有效样本 json 文件转换为十六进制流
        :return: dict(), 规则 ID 及其对应的 HTTP 请求十六进制流的字典, {"13060028":"47 45 54 20 2f 69 ...", ...}
        """
        # TODO: 多个 HTTP 请求的现在先不处理
        http_pcap_dict = AutoTester.get_http_headers_dict(self.test_json_file)

        for each_pcap, each_http_request in http_pcap_dict.items():
            if len(each_http_request) > 1:  # 不止一个 HTTP 请求, 暂时不处理
                print("[!] 忽略 {}".format(each_pcap))
            else:
                http_pcap_dict[each_pcap] = self.create_hex_stream(each_http_request[0])

        return http_pcap_dict

    def get_all_fields(self, pcap_path, http_request):
        """
        从 pcap_path 以及 http_request 提取出数据库字段对应的值
        :param pcap_path: pcap_path, 形式如: "./waf/13020058.pcap", 可以提取出类型/规则
        :param http_request: "33 44 55 66", 不太好提取了, 只能作为规则内容字段了
        :return: rule_type, version, protocol, port, rule_id, rule_content
        """
        result = re.findall("[^/]*/([wafips]{3})/([0-9_]*).pcap", pcap_path, flags=re.IGNORECASE)[0]
        return result[0], "20160101", "TCP", "80", result[1], http_request

    def get_all_data_db_need(self, result_dict):
        """
        获取将要写入数据库的所有数据
        # 规则类型: WAF/IPS/UTM/PVS
        # 版本号: 规则 pcap 包的 zip 版本号
        # 协议: TCP
        # 端口号: 80
        # 规则 ID: ...
        # HTTP 请求: ...
        :param result_dict: 自动化测试模块得到的 dict 数据, 可以从里面提取出规则/版本号等信息
        :return: list(), 每个元素都是命名元组, 包括数据库所需的各个字段
        """
        result_list = list()
        demo_rule = namedtuple("demo_rule", ["rule_type",
                                             "version",
                                             "protocol",
                                             "port",
                                             "rule_id",
                                             "rule_content"])

        for pcap_path, http_request in result_dict.items():
            all_fields = self.get_all_fields(pcap_path, http_request)
            result_list.append(demo_rule(*all_fields))

        return result_list

    def create_sqlite_lib_file(self):
        """
        创建 lib 文件
        :return:
        """
        # 读取 json 数据, 解析为字典形式, 字典的键为规则 ID, 值为 HTTP 请求的十六进制流
        result_dict = self.format_json_file_to_hex_stream()

        # 提取每一个字段, 目前实现的字段:
        all_data = self.get_all_data_db_need(result_dict)

        # 写入数据库
        for each_row in all_data:
            print(each_row)


if __name__ == "__main__":
    des_key = des_cbc_iv = "sangfor*"
    lc = LibCreator(des_key, des_cbc_iv, "efficient_pcap.json")
    lc.create_sqlite_lib_file()
