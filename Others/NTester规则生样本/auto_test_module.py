#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.11 开始添加 UTM 的支持, 比如说发送 DNS 数据包的功能
2017.01.10 支持 SSH 连接执行命令了, 支持阻塞, 目前每次发包前都有些准备工作, 比如 清除日志/提权/加速日志 等操作
2017.01.10 优化交互信息, 修复特殊 HTTP 请求会导致报错的 BUG, 支持 IPS 了
2017.01.09 基本完成了自动化测试流程, 但是还需要完善, 比如说最后生成的 json 文件, 最好是用命名元组的格式展现, 方便之后写入数据库
2017.01.02 开始自动化测试模块
"""
try:
    import simplejson as json
except ImportError:
    import json

import requests
import paramiko
import time
import pymysql
import re
import datetime
import scapy.sendrecv
from scapy.layers.inet import IP, UDP
from scapy.layers.dns import DNS, DNSQR
from pcap_scapy_parse import PcapParser
from requests.exceptions import ConnectTimeout, ReadTimeout, ConnectionError

__author__ = '__L1n__w@tch'

TIMEOUT = 15  # 等待一段时间再查日志


# TODO: 提供 sockets 丢包的方法
# TODO: 至少两处需要重构
# TODO: 重构 + 添加 verbose 选项
# TODO: MySQL 连不上, 因为监听只在 127.0.0.1 上, 需要更改
# TODO: 不支持输出文件的文件名指定
# TODO: target_ip 需要重构

class AutoTester:
    def __init__(self, result_json_file_path, af_back_info, af_mysql_info):
        """
        :param af_back_info: 连接 af 后台所需的一切信息
        :param result_json_file_path: 解析 pcap 包得到的 json 格式文件
        :param af_mysql_info: 连接 af MySQL 所需的一切信息
        """
        self.test_json_file = result_json_file_path
        self.af_mysql_info = af_mysql_info
        self.af_back_information = af_back_info
        self.af_mysql_connect = None  # 用于 mysql 连接
        self.af_back_connect = None  # 用于 af 后台连接

    @staticmethod
    def get_http_headers_dict(json_file_path):
        """
        从 json 文件中读取每一个 http 头放到字典中
        :param json_file_path: json 文件路径
        :return: dict(), 每一个元素是一个 http 头及其 pcap 包
        """
        with open(json_file_path, "r") as f:
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
        post_data = http_header.split("\r\n\r\n", 1)
        if len(post_data) > 1:
            return post_data[1]
        else:
            return ""

    def send_post_request(self, http_header, ip, verbose=False):
        """
        发送 POST 请求
        :param http_header: 要发送的 post 请求头
        :param ip: 目标 IP
        """
        # TODO: 需要跟 GET 请求进行重构
        url, header = self.parse_http_header(http_header)
        post_data = self.get_post_data_from_http_header(http_header)

        # 有些请求是 POST test.pl HTTP/1.0 这种的, 提取出来没有根路径导致报错
        if url.startswith("/"):
            attack_url = "http://{}{}".format(ip, url)
        else:
            attack_url = "http://{}/{}".format(ip, url)

        print("[*] 发送 POST 请求: {}".format(attack_url))

        try:
            response = requests.post(attack_url, headers=header, data=post_data, timeout=3)
        except (ConnectTimeout, ReadTimeout, ValueError, ConnectionError):
            if verbose:
                print("[!] 发送 POST 请求失败: {}".format(attack_url))

    def send_get_request(self, http_header, ip, verbose=False):
        """
        发送 GET 请求
        :param http_header: 要发送的 get 请求头
        :param ip: 目标 IP
        """
        # TODO: 需要跟 POST 请求进行重构
        url, header = self.parse_http_header(http_header)

        # 有些请求是 GET test.pl HTTP/1.0 这种的, 提取出来没有根路径导致报错
        if url.startswith("/"):
            attack_url = "http://{}{}".format(ip, url)
        else:
            attack_url = "http://{}/{}".format(ip, url)

        print("[*] 发送 GET 请求: {}".format(attack_url))

        try:
            response = requests.get(attack_url, headers=header, timeout=3)
        except (ConnectTimeout, ReadTimeout, ValueError, ConnectionError):
            if verbose:
                print("[!] 发送 GET 请求失败: {}".format(attack_url))

    @staticmethod
    def get_sid_from_pcap_name(pcap_name):
        """
        从 pcap_name 中获取 sid
        :param pcap_name: str(), "waf/13010007.pcap"
        :return: str(), "13010007.pcap"
        """
        sid = re.findall(".*?/?([0-9_]*).pcap", pcap_name)[0]
        if "_" in sid:
            sid = sid.split("_")[0]
        return sid

    def verify_waf_ips_packet(self, verbose=False):
        """
        验证 waf 和 ips 包和日志是否对应上
        """
        # 初始化
        http_headers_dict = self.get_http_headers_dict(self.test_json_file)
        efficient_pcap = dict()

        # 一个一个验证
        print("[*] 开始进行验证")
        db_sid_list = self.af_mysql_connect.get_all_sid_in_log_tables(["WAF", "IPS"])
        for each_pcap, each_pcap_https in http_headers_dict.items():
            sid = self.get_sid_from_pcap_name(each_pcap)
            if sid in db_sid_list:
                print("[*] 验证 sid-{} 有对应的有效 pcap 包".format(sid))

                # 是有效请求, 记录相应信息
                efficient_pcap.setdefault(each_pcap, list())
                efficient_pcap[each_pcap].extend(each_pcap_https)
            elif verbose:
                print("[!] 该 sid-{} 在数据库中查找不到".format(sid))

        # 记录
        # TODO: 文件名怎么写死了
        with open("efficient_pcap.json", "w") as f:
            json.dump(efficient_pcap, f)

    def verify_pcap_all_together(self, ip, verbose=False):
        """
        一口气把所有的包都扔过去, 然后再验证哪些规则有效
        :param ip: 目标 IP, 构造请求时使用
        :return:
        """
        # TODO: 需要重构, 已经新编了一个丢包和验证的子方法了
        # 初始化
        http_headers_dict = self.get_http_headers_dict(self.test_json_file)
        efficient_pcap = dict()

        # 扔包
        print("[*] 开始丢包")
        for each_pcap, each_pcap_https in http_headers_dict.items():
            for each_http in each_pcap_https:
                self.send_request(each_http, ip)

        print("[*] 丢包完成")
        print("[*] 等待 {} s".format(TIMEOUT))
        time.sleep(TIMEOUT)

        # 一个一个验证
        print("[*] 开始进行验证")
        db_sid_list = self.af_mysql_connect.get_all_sid_in_log_tables(["WAF", "IPS"])
        for each_pcap, each_pcap_https in http_headers_dict.items():
            sid = self.get_sid_from_pcap_name(each_pcap)
            if sid in db_sid_list:
                print("[*] 验证 sid-{} 有对应的有效 pcap 包".format(sid))

                # 是有效请求, 记录相应信息
                efficient_pcap.setdefault(each_pcap, list())
                efficient_pcap[each_pcap].extend(each_pcap_https)
            elif verbose:
                print("[!] 该 sid-{} 在数据库中查找不到".format(sid))

        # 记录
        # TODO: 文件名怎么写死了
        with open("efficient_pcap.json", "w") as f:
            json.dump(efficient_pcap, f)

    def verify_pcap_each_by_each(self, ip, result_to_file=True):
        """
        验证每一个 pcap 包, 如果是有效的则进入样本库, 这种方式是一个一个验证的, 效率极低, 但是精确度会高一些(不保证100%, 原因是等待时间不确定)
        :param ip: 目标 IP, 构造请求时使用
        :param result_to_file: True or False, 标记是否把输出结果打印到文件中, 方便排查, True 表示写到调试文件中
        """
        http_headers_dict = self.get_http_headers_dict(self.test_json_file)
        efficient_pcap = dict()

        # TODO: 调试文件名是写死的
        with open("pcap_each_by_each_debug_file.txt", "w") as f:
            # 遍历每一个 HTTP 头
            for each_pcap, each_pcap_https in http_headers_dict.items():
                print("[*] 测试: {}".format(each_pcap), file=f) if result_to_file else None
                sid = self.get_sid_from_pcap_name(each_pcap)
                for each_http in each_pcap_https:
                    if self.is_efficient_http_request(each_http, ip, sid):
                        # 是有效请求, 记录相应信息
                        efficient_pcap.setdefault(each_pcap, list())
                        efficient_pcap[each_pcap].append(each_http)
                        print("[*] {sep} 规则 {0} 有效 {sep}, 攻击为 {1}".format(sid, each_http, sep="*" * 30)
                              , file=f) if result_to_file else None
                    else:
                        print("[!] {sep} 规则 {0} 无效 {sep}, 攻击为 {1}".format(sid, each_http, sep="*" * 30)
                              , file=f) if result_to_file else None

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

    def af_back_prepare(self, local_ip_address):
        """
        进行一些 af 后台的预备操作, 比如清除数据库日志/加快日志创建速度等
        """
        af_ssh_connect = AFSSHConnector(*self.af_back_information)

        # 依次是: 清除数据库/提权/生成日志加速
        prepare_commands = ["/usr/sbin/re_install_mysql.sh",
                            ("/virus/mysql/bin/mysql -uroot -proot -e \"use mysql; "
                             "GRANT ALL ON *.* to root@'{}' IDENTIFIED BY 'root'; "
                             "FLUSH PRIVILEGES;\"".format(local_ip_address)),
                            "touch /var/often_write/quick_load.flag"]

        af_ssh_connect.connect_then_execute_many_commands(prepare_commands)

    def send_waf_ips_utm_packet(self, target_ip):
        """
        进行 waf/ips/utm 的丢包操作
        :param target_ip: 测试主机的 IP
        :return:
        """
        print("[*] 开始丢 waf/ips 包")
        http_headers_dict = self.get_http_headers_dict(self.test_json_file)

        for each_pcap, each_pcap_https in http_headers_dict.items():
            for each_http in each_pcap_https:
                self.send_request(each_http, target_ip)

        print("[*] 开始丢 utm 包")
        # 获取所有 urls
        all_urls_list = self.get_all_utm_urls("utm_url_result.json")

        # 把所有 urls 丢过去
        for each_utm_url in all_urls_list:
            self.send_request_with_host(each_utm_url, target_ip)

    def run(self, local_ip, target_ip):
        """
        完成自动化测试流程, 这个方法先把所有类型的包丢出去, 然后再依次进行验证
        :param local_ip: 本地 IP 地址
        :param target_ip: 测试服务器的 IP 地址
        """
        print("[*] 进行验证阶段必要的初始化工作")
        # AF 后台准备工作
        self.af_back_prepare(local_ip)

        # 初始化 MySQL 连接实例
        self.af_mysql_connect = AFMySQLQuery(*self.af_mysql_info)

        print("[*] 开始进行丢包操作")
        self.send_waf_ips_utm_packet(target_ip)

        print("[*] 丢包完成, 等待 {}s 后开始验证".format(TIMEOUT))
        time.sleep(TIMEOUT)

        # 验证 IPS/WAF
        print("[*] 开始验证 waf/ips")
        self.verify_waf_ips_packet()

        # 验证 UTM
        print("[*] 开始验证 utm")
        self.verify_utm_packet()

        print("[*] 自动化验证阶段结束")

    def run2(self, local_ip, target_ip):
        """
        完成自动化测试流程, 这个方法区别于 run, 这个方法先验证 waf/ips, 之后才验证 utm
        :param local_ip: 本地 IP 地址
        :param target_ip: 测试服务器的 IP 地址
        """
        # AF 后台准备工作
        self.af_back_prepare(local_ip)

        # 初始化 MySQL 连接实例
        self.af_mysql_connect = AFMySQLQuery(*self.af_mysql_info)

        # 解析 HTTP 请求头, 按照 requests 库封装好并发送出去
        # 验证 IPS/WAF
        # TODO: 加个可选项, 选择一口气全部扔过去还是一个一个扔
        print("[*] 开始验证 waf/ips")
        self.verify_pcap_all_together(target_ip)  # 全部扔过去再一个一个验证
        # self.verify_pcap_each_by_each(target_ip)  # 一个一个扔包后再验证

        # 验证 UTM
        print("[*] 开始验证 utm")
        self.verify_utm_urls_all_together(target_ip)

    @staticmethod
    def is_efficient_utm_url(url, utm_log_data):
        """
        判断 url 是否有效
        :param url: 要查询的 url
        :param utm_log_data: 从 utm 表中获取到的 sid 及其 result
        :return: str() or False, False 表示没有查到 sid 号, str() 表示 sid 号本身
        """
        for sid, result in utm_log_data:
            if url in result:
                return sid
        return False

    def get_efficient_urls_sids_dict(self, urls):
        """
        根据 url 查询 utm 日志, 如果存在于日志中, 说明 url 有效, 同时提取出 sid 号
        :param urls:
        :return: dict(), 键为 sid 号, 值为对应的 url
        """
        result_dict = dict()

        # 获取数据库中所有数据
        print("[*] 开始获取数据库 utm 表中所有记录")
        all_utm_log = self.af_mysql_connect.get_all_sid_and_result_in_utm_table()

        print("[*] 开始判断 utm url 是否有效")
        # 依次判断每一条 url 是否有效
        for each_utm_url in urls:
            sid = self.is_efficient_utm_url(each_utm_url, all_utm_log)
            if sid is not False:
                result_dict[sid] = each_utm_url

        return result_dict

    def verify_utm_packet(self):
        """
        验证 utm 包和日志是否对应上
        :return:
        """
        # 获取所有 urls
        all_urls_list = self.get_all_utm_urls("utm_url_result.json")

        # 查询日志, 提取出有效的 url 及 sid 信息
        valid_url_dict = self.get_efficient_urls_sids_dict(all_urls_list)

        # 把有效的 urls 保存下来
        with open("efficient_utm_urls.json", "w") as f:
            json.dump(valid_url_dict, f)

    def verify_utm_urls_all_together(self, target_ip):
        """
        验证所有 utm urls 是否有效
        :param target_ip: 测试用的目标 IP
        :return:
        """
        # TODO: 需要重构, 已经有一个丢包和验证的子方法了
        # 获取所有 urls
        all_urls_list = self.get_all_utm_urls("utm_url_result.json")

        # 把所有 urls 丢过去
        for each_utm_url in all_urls_list:
            self.send_request_with_host(each_utm_url, target_ip)

        # 查询日志, 提取出有效的 url 及 sid 信息
        valid_url_dict = self.get_efficient_urls_sids_dict(all_urls_list)

        # 把有效的 urls 保存下来
        with open("efficient_utm_urls.json", "w") as f:
            json.dump(valid_url_dict, f)

    @staticmethod
    def send_dns_query_packet(dns_server_ip, query_domain):
        """
        发送 DNS 咨询数据包, 不检查结果
        :param dns_server_ip: DNS 服务器的 IP 地址
        :param query_domain: 要询问的域名
        """
        scapy.sendrecv.send(IP(dst=dns_server_ip) / UDP() / DNS(rd=1, qd=DNSQR(qname=query_domain)))

    @staticmethod
    def get_host_from_url(url, verbose=False):
        """
        从 URL 中提取域名
        :param url: str(), 要提取的 url
        :param verbose: 是否打印详细信息
        :return: str(), url 中的 host
        """
        if verbose is True:
            print("[*] 尝试解析 url {}".format(url))

        url = str(url)
        if "/" in url:
            host, path = url.split("/", maxsplit=1)
        else:
            host, path = url, ""
        return host, "{}".format(path)

    def send_request_with_host(self, url, target_ip, verbose=False):
        """
        发送一个 GET 请求, 带 HOST 字段的, 主要是用来测试 UTM 的
        :param url: 要发送的 URL, 会自动提取 host 字段
        :param target_ip: 往哪个 IP 丢包
        :param verbose: True or False, 表示是否打印详细信息
        :return:
        """
        domain, path = self.get_host_from_url(url)

        url = "http://{}/{}".format(target_ip, path)
        headers = {
            "Host": "{}".format(domain),
            "User-Agent": "User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        }

        print("[*] 访问 {}, 域名为 {}".format(url, domain))

        try:
            response = requests.get(url, headers=headers, timeout=3)
        except (ConnectTimeout, ReadTimeout, ValueError, ConnectionError):
            if verbose:
                print("[!] 发送 GET 请求失败: {}".format(url))

    @staticmethod
    def get_all_utm_urls(json_file_path):
        """
        从 json 文件中获取所有 urls 放在一个列表里
        :param json_file_path: str(), json 文件路径
        :return: list(), 每一个元素是一个 utm url
        """
        with open(json_file_path, "r") as f:
            data = json.load(f)
        return data


class AFMySQLQuery:
    def __init__(self, af_ip, mysql_user, mysql_pw, db_name):
        self.af_ip = af_ip
        self.mysql_user = mysql_user
        self.mysql_pw = mysql_pw
        self.db_name = db_name
        self.client = None  # 连接 mysql 的实体对象

    @staticmethod
    def is_table_exists(cursor, table_name):
        """
        判断某一个表是否存在
        :param cursor: 游标
        :param table_name: 要判断的表
        :return: True or False
        """
        cursor.execute("show tables like '{}'".format(table_name))
        data = cursor.fetchall()
        return len(data) > 0

    def get_log_table_name_list(self):
        """
        获取指定库当天日期的表格名字
        :return: list(), 每一个元素是一个指定库的表格名字, ["X20170110", "I20170110"]
        """
        today = self.get_today_date()
        table_name_list = list()

        # WAF 库
        table_name_list.append("X{}".format(today))

        # IPS 库
        table_name_list.append("I{}".format(today))

        return table_name_list

    def get_all_sid_in_log_tables(self, table_name_list):
        """
        从日志表中获取所有 sid 号
        :param table_name_list: list(), 指定要获取的日志类型, 比如 ["WAF", "IPS"]
        :return: list(), 保存所有的 sid
        """
        result_sid_list = list()

        # 获取 WAF 的所有 sid
        result_sid_list.extend(self.get_all_sid_in_waf_log())

        # 获取 IPS 的所有 sid
        result_sid_list.extend(self.get_all_sid_in_ips_log())

        return result_sid_list

    def get_all_sid_in_ips_log(self):
        """
        获取 waf 数据库中所有 sid 号
        :return: list(), 保存所有 sid
        """
        # TODO: 需要重构, 跟 waf 的区别仅仅是表名以及字段名
        today = self.get_today_date()
        result_sid_list = list()

        with pymysql.connect(self.af_ip, self.mysql_user, self.mysql_pw, self.db_name) as cursor:
            if self.is_table_exists(cursor, "I{}".format(today)):
                # 执行 SQL 查询
                cursor.execute(
                    "SELECT hole_id FROM I{} WHERE record_time > '00:00' AND record_time < '23:59'".format(today)
                )
                data = cursor.fetchall()

                # 保存 ID 号
                for each_log in data:
                    if len(each_log) > 0:
                        log_sid = each_log[0]
                        result_sid_list.append(str(log_sid))

        return result_sid_list

    def get_all_sid_in_waf_log(self):
        """
        获取 waf 数据库中所有 sid 号
        :return: list(), 保存所有 sid
        """
        # TODO: 需要重构, 跟 ips 的区别仅仅是表名以及字段名
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

    def get_attack_type_from_waf_log(self, cursor, sid):
        """
        通过 sid 号获取 waf 日志中对应记录的 attack_type
        :param cursor: 游标对象
        :param sid: 规则 ID 号
        :return: str(), catagory_id 号
        """
        # TODO: 需要重构, 跟 ips 的区别仅仅是表名以及字段名
        today = self.get_today_date()

        sql = "SELECT attack_type FROM X{} WHERE sid = {} AND record_time > '00:00' AND record_time < '23:59'" \
            .format(today, sid)

        cursor.execute(sql)

        data = cursor.fetchone()

        return data[0]

    def get_attack_type_from_ips_log(self, cursor, sid):
        """
        通过 sid 号获取 ips 日志中对应记录的 attack_type
        :param cursor: 游标对象
        :param sid: 规则 ID 号
        :return: str(), catagory_id 号
        """
        # TODO: 需要重构, 跟 ips 的区别仅仅是表名以及字段名
        today = self.get_today_date()

        sql = "SELECT attack_type FROM I{} WHERE hole_id = {} AND record_time > '00:00' AND record_time < '23:59'" \
            .format(today, sid)

        cursor.execute(sql)

        data = cursor.fetchone()

        # 查询不到的话, 检查是不是数据库日志被清空了?
        assert len(data) > 0

        return data[0]

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

    def connect(self):
        """
        建立连接, 需要后续用户自行 close 掉
        """
        if self.client is None:
            self.client = pymysql.connect(self.af_ip, self.mysql_user, self.mysql_pw, self.db_name)

        return self.client.cursor()

    def close_connect(self):
        """
        关闭 db 连接操作
        """
        if self.client:
            self.client.close()

    def get_all_sid_and_result_in_utm_table(self):
        """
        从 utm 表格中获取所有数据, 仅获取 sid 字段及 result 字段
        :return: list(), [(sid1, result1), (sid2, result2), ...]
        """
        today = self.get_today_date()
        result_list = list()

        with pymysql.connect(self.af_ip, self.mysql_user, self.mysql_pw, self.db_name) as cursor:
            if self.is_table_exists(cursor, "T{}".format(today)):
                # 执行 SQL 查询
                cursor.execute(
                    "SELECT sid, result FROM T{} WHERE record_time > '00:00' AND record_time < '23:59'".format(today)
                )
                data = cursor.fetchall()

                return list(data)

        return result_list

    def is_url_in_utm_result(self, url, cursor):
        """
        查询 utm 表, 判断 url 是否存在于 utm 数据库中 result 字段中
        :param url: str(), 要判断的 url
        :param cursor: 游标对象
        :return: str() or False, False 表示不存在, str() 表示 sid 号
        """
        today = self.get_today_date()

        sql = "SELECT sid,result FROM T{} WHERE result REGEXP \"{}\"".format(today, url)

        cursor.execute(sql)
        data = cursor.fetchone()
        if len(data) > 0:
            return data[0]  # 返回 sid

        assert False  # 这个方法还没写完, 只是留了个模型


class AFSSHConnector:
    def __init__(self, host_name, port, user_name, password):
        self.host_name = host_name
        self.port = port
        self.user_name = user_name
        self.password = password
        self.client = None  # socket 对象

    def connect(self):
        """
        建立 SSH 连接, 注意后续需要手动使用 client.close() 关闭 ssh 连接
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.host_name, port=self.port, username=self.user_name, password=self.password)

        return client

    def execute_command(self, command):
        """
        执行命令
        :param command: str(), 要执行的命令
        """
        if self.client is None:
            self.client = self.connect()

        command_result = str()

        stand_in, stand_out, stand_error = self.client.exec_command(command)
        for std in stand_out.readlines():
            command_result += std

        return command_result

    def connect_then_execute_many_commands(self, commands, verbose=False):
        """
        执行许多命令, 不检查执行结果
        :param commands: list(), 每一个元素是一条命令
        """
        with paramiko.SSHClient() as client:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.host_name, port=self.port, username=self.user_name, password=self.password)

            for each_command in commands:
                print("[*] 执行命令: {}".format(each_command))
                stand_in, stand_out, stand_error = client.exec_command(each_command)
                for output in stand_out.readlines():
                    if verbose:
                        print("[*] 执行结果: {}".format(output), end="")


if __name__ == "__main__":
    af_mysql_information = ("192.192.90.134", "root", "root", "FW_LOG_fwlog")
    af_back_information = ("192.192.90.134", 22345, "admin", "1")
    at = AutoTester("2th_headers_result.json", af_back_information, af_mysql_information)
    at.run(local_ip="192.192.90.135", target_ip="192.168.116.2")
