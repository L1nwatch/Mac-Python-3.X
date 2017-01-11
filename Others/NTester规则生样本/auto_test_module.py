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
# TODO: 添加 verbose 选项, 现在打印的消息有点多
# TODO: MySQL 连不上, 因为监听只在 127.0.0.1 上, 需要更改
# TODO: 不支持输出文件的文件名指定
# TODO: 不支持 UTM 库的测试

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

    def send_post_request(self, http_header, ip):
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
            print("[!] 发送 POST 请求失败: {}".format(attack_url))

    def send_get_request(self, http_header, ip):
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

    def verify_pcap_all_together(self, ip):
        """
        一口气把所有的包都扔过去, 然后再验证哪些规则有效
        :param ip: 目标 IP, 构造请求时使用
        :return:
        """
        # 初始化
        http_headers_dict = self.get_http_headers_dict(self.test_json_file)
        efficient_pcap = dict()

        # 扔包
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
            else:
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

    def run(self, local_ip, target_ip):
        """
        完成自动化测试流程
        :param local_ip: 本地 IP 地址
        :param target_ip: 测试服务器的 IP 地址
        """
        # AF 后台准备工作
        self.af_back_prepare(local_ip)

        # 初始化 MySQL 连接实例
        self.af_mysql_connect = AFMySQLQuery(*self.af_mysql_info)

        # 解析 HTTP 请求头, 按照 requests 库封装好并发送出去
        # TODO: 加个可选项, 选择一口气全部扔过去还是一个一个扔
        self.verify_pcap_all_together(target_ip)  # 全部扔过去再一个一个验证
        # self.verify_pcap_each_by_each(target_ip)  # 一个一个扔包后再验证

    @staticmethod
    def send_dns_query_packet(dns_server_ip, query_domain):
        """
        发送 DNS 咨询数据包, 不检查结果
        :param dns_server_ip: DNS 服务器的 IP 地址
        :param query_domain: 要询问的域名
        """
        scapy.sendrecv.send(IP(dst=dns_server_ip) / UDP() / DNS(rd=1, qd=DNSQR(qname=query_domain)))


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

    def connect_then_execute_many_commands(self, commands):
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
                    print("[*] 执行结果: {}".format(output), end="")


if __name__ == "__main__":
    af_mysql_information = ("192.192.90.134", "root", "root", "FW_LOG_fwlog")
    af_back_information = ("192.192.90.134", 22345, "admin", "1")
    at = AutoTester("2th_headers_result.json", af_back_information, af_mysql_information)
    # at.run(local_ip="192.192.90.135", target_ip="192.168.116.2")
    at.send_dns_query_packet("112.113.114.115", "www.baidu.com")
