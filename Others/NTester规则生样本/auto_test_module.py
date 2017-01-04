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
import time
import pymysql
import re
import datetime
from pcap_scapy_parse import PcapParser
from requests.exceptions import ConnectTimeout,ReadTimeout

__author__ = '__L1n__w@tch'

TIMEOUT = 15  # 等待一段时间再查日志


class AutoTester:
    def __init__(self, result_json_file_path, af_mysql_info):
        """
        :param result_json_file_path: 解析 pcap 包得到的 json 格式文件
        :param af_mysql_info: 连接 af MySQL 所需的一切信息
        """
        self.test_json_file = result_json_file_path
        self.af_mysql_info = af_mysql_info
        self.af_mysql_connect = None  # 用于 mysql 连接

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
        # print("{sep}POST 数据: {0}".format(post_data, sep=" " * 8))

        try:
            response = requests.post(attack_url, headers=header, data=post_data, timeout=3)
        except (ConnectTimeout, ReadTimeout):
            pass

    def send_get_request(self, http_header, ip):
        """
        发送 GET 请求
        :param http_header: 要发送的 get 请求头
        :param ip: 目标 IP
        """
        url, header = self.parse_http_header(http_header)
        attack_url = "http://{}{}".format(ip, url)
        print("    GET 攻击: {}".format(attack_url))

        try:
            response = requests.get(attack_url, headers=header, timeout=3)
        except (ConnectTimeout,ReadTimeout):
            pass

    @staticmethod
    def get_sid_from_pcap_name(pcap_name):
        """
        从 pcap_name 中获取 sid
        :param pcap_name: str(), "waf/13010007.pcap"
        :return: str(), "13010007.pcap"
        """
        sid = re.findall(".*/([0-9_]*).pcap", pcap_name)[0]
        return sid

    def verify_pcap_all_together(self, ip):
        """
        一口气把所有的包都扔过去, 然后再验证哪些规则有效
        :param ip: 目标 IP, 构造请求时使用
        :return:
        """
        # 初始化
        http_headers_dict = self.get_http_headers_dict()
        efficient_pcap = dict()

        # 扔包
        for each_pcap, each_pcap_https in http_headers_dict.items():
            for each_http in each_pcap_https:
                self.send_request(each_http, ip)

        print("[!] 丢包完成")
        print("[!] 等待 {} s".format(TIMEOUT))
        time.sleep(TIMEOUT)

        # 一个一个验证
        db_sid_list = self.af_mysql_connect.get_all_sid_in_waf_log()
        for each_pcap, each_pcap_https in http_headers_dict.items():
            sid = self.get_sid_from_pcap_name(each_pcap)
            if sid in db_sid_list:
                # 是有效请求, 记录相应信息
                efficient_pcap.setdefault(each_pcap, list())
                efficient_pcap[each_pcap].extend(each_pcap_https)

        # 记录
        with open("efficient_pcap.json", "w") as f:
            json.dump(efficient_pcap, f)

    def verify_pcap_each_by_each(self, ip):
        """
        验证每一个 pcap 包, 如果是有效的则进入样本库, 这种方式是一个一个验证的, 效率极低, 但是精确度会高一些(不保证100%, 原因是等待时间不确定)
        :param ip: 目标 IP, 构造请求时使用
        """
        http_headers_dict = self.get_http_headers_dict()
        efficient_pcap = dict()

        # 遍历每一个 HTTP 头
        for each_pcap, each_pcap_https in http_headers_dict.items():
            print("测试: {}".format(each_pcap))
            sid = self.get_sid_from_pcap_name(each_pcap)
            for each_http in each_pcap_https:
                if self.is_efficient_http_request(each_http, ip, sid):
                    # 是有效请求, 记录相应信息
                    efficient_pcap.setdefault(each_pcap, list())
                    efficient_pcap[each_pcap].append(each_http)
                    print("{sep} 规则 {0} 有效 {sep}".format(sid, sep="*" * 30))
                    # print("规则 {} 生效, pcap 包为: {}, http 请求为: {}".format(sid, each_pcap, each_http))

        with open("efficient_pcap.json", "w") as f:
            json.dump(efficient_pcap, f)

    def send_request(self, http_packet, ip):
        """
        发送请求, 自动识别是 POST 还是 GET 请求
        :param http_packet: http 包
        :param ip: 测试用的目标 IP
        """
        # POST 请求
        if PcapParser.is_http_post_request_header(http_packet):
            # 攻击之后判断 sid 存在于数据库中
            self.send_post_request(http_packet, ip)
        # GET 请求
        elif PcapParser.is_http_get_request_header(http_packet):
            self.send_get_request(http_packet, ip)
        # 其他请求
        else:
            raise RuntimeError("遇到无法解析的 HTTP 头了")

    def is_efficient_http_request(self, http_packet, ip, sid):
        """
        判断是否是一个有效的 pcap 包, 即发送该包能产生对应规则 ID
        :param http_packet: http 包
        :param ip: 测试用的目标 IP
        :param sid: 期望匹配的规则 ID
        :return: True or False, True 表示该包有效
        """
        if self.af_mysql_connect.is_sid_in_waf_log(sid) is False:
            self.send_request(http_packet, ip)
            time.sleep(TIMEOUT)
            return self.af_mysql_connect.is_sid_in_waf_log(sid)
        return False

    def run(self, target_ip):
        """
        完成自动化测试流程
        :param target_ip: 测试服务器的 IP 地址
        """
        # 初始化 MySQL 连接实例
        self.af_mysql_connect = AFMySQLQuery(*self.af_mysql_info)

        # 解析 HTTP 请求头, 按照 requests 库封装好并发送出去
        self.verify_pcap_all_together(target_ip)  # 全部扔过去再一个一个验证
        # self.verify_pcap_each_by_each(target_ip)  # 一个一个扔包后再验证


class AFMySQLQuery:
    def __init__(self, af_ip, mysql_user, mysql_pw, db_name):
        self.af_ip = af_ip
        self.mysql_user = mysql_user
        self.mysql_pw = mysql_pw
        self.db_name = db_name

    @staticmethod
    def is_table_exists(cursor, table_name):
        """
        判断某一个表是否存在
        :param cursor: 游标
        :param table_name: 要判断的表
        :return: True or False
        """
        cursor.execute("show tables like '%{}%'".format(table_name))
        data = cursor.fetchall()
        return len(data) > 0

    def get_all_sid_in_waf_log(self):
        """
        获取 waf 数据库中所有 sid 号
        :return: list(), 保存所有 sid
        """
        today = self.get_today_date()
        result_sid_list = list()

        with pymysql.connect(self.af_ip, self.mysql_user, self.mysql_pw, self.db_name) as cursor:
            if self.is_table_exists(cursor, "X{}".format(today)):
                # 执行 SQL 查询
                cursor.execute(
                    "SELECT sid FROM X{} WHERE record_time > '00:00' AND record_time < '23:59'".format(today)
                )
                data = cursor.fetchall()

                # 保存 ID 号
                for each_log in data:
                    if len(each_log) > 0:
                        log_sid = each_log[0]
                        result_sid_list.append(str(log_sid))

        return result_sid_list

    def is_sid_in_waf_log(self, sid):
        """
        判断 sid 号是否存在于 waf 日志中
        :param sid: str(), such as 13010007
        :return: True or False
        """
        today = self.get_today_date()

        with pymysql.connect(self.af_ip, self.mysql_user, self.mysql_pw, self.db_name) as cursor:
            if self.is_table_exists(cursor, "X{}".format(today)):
                # 执行 SQL 查询
                cursor.execute(
                    "SELECT sid FROM X{} WHERE record_time > '00:00' AND record_time < '23:59'".format(today)
                )
                data = cursor.fetchall()
                # 判断 ID 号
                for each_log in data:
                    log_sid = each_log[0]
                    if sid == str(log_sid):
                        return True
            return False

    @staticmethod
    def get_today_date():
        """
        获取当天日期
        :return: str(), 20170104
        """
        today = datetime.datetime.now()
        return "{}{}{}".format(str(today.year).zfill(4), str(today.month).zfill(2), str(today.day).zfill(2))


if __name__ == "__main__":
    af_mysql_info = ("192.192.89.134", "root", "root", "FW_LOG_fwlog")
    at = AutoTester("2th_headers_result.json", af_mysql_info)
    at.run("192.168.116.2")
