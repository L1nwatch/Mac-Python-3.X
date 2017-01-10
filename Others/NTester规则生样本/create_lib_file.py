#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.10 支持指定数据库名/表名了; 支持 catagory_id 及 module_id 字段的获取
2017.01.09 完善整个生成样本库的流程, 包括解析 json 到生成数据库所需的全部字段, 生成数据库以及写入数据库
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
from auto_test_module import AutoTester, AFMySQLQuery
from collections import namedtuple

__author__ = '__L1n__w@tch'


# TODO: 目前还不支持 APT 数据库字段的填充
# TODO: 多个 HTTP 请求的现在先不处理
# TODO: 还不支持 cve_id 的提取
# TODO: 添加 verbose 选项, 现在打印的消息有点多, 另外需要加入 logger 负责打印信息的


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
        self.mysql = None  # 连接 MySQL 的实体对象
        self.sample_http_obj = namedtuple("sample_http_obj", ["Catagory_id", "Request", "Response",
                                                              "Attack", "Isvalid", "From", "Module",
                                                              "CveID", "Sid", "Port", "Protocol", "Action"])

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
        result_dict = dict()
        http_pcap_dict = AutoTester.get_http_headers_dict(self.test_json_file)

        for each_pcap, each_http_request in http_pcap_dict.items():
            if len(each_http_request) > 1:  # 不止一个 HTTP 请求, 暂时不处理
                print("[!] 忽略多于一个 HTTP 请求的包: {}".format(each_pcap))
            else:
                result_dict[each_pcap] = self.create_hex_stream(each_http_request[0])

        return result_dict

    @staticmethod
    def get_module_id(module_name):
        """
        根据 module name 获取 module id
        :param module_name:  模块名字, 比如 WAF/IPS 等
        """
        module_dict = {"WAF": 3, "IPS": 2, "PVS": 4, "APT": 1}
        return module_dict[str(module_name).upper()]

    def get_catagory_id(self, sid, rule_type):
        """
        根据 sid 获取对应的 attack_type(即 catagory_id)
        :param sid: str(), sid 规则号
        :param rule_type: str(), 攻击类型, 决定了从哪个表格获取, 比如 WAF 是 X20170110, IPS 是 I20170110 等
        :return: str(), catagory_id 号, 比如 10
        """
        cursor = self.mysql.connect()

        if rule_type.upper() == "WAF":
            catagory_id = self.mysql.get_attack_type_from_waf_log(cursor, sid)
        elif rule_type.upper() == "IPS":
            catagory_id = self.mysql.get_attack_type_from_ips_log(cursor, sid)
        else:
            raise RuntimeError("还不支持该类型 {}".format(rule_type))

        return catagory_id

    def get_all_fields(self, pcap_path, http_request):
        """
        从 pcap_path 以及 http_request 提取出数据库字段对应的值
        :param pcap_path: pcap_path, 形式如: "./IPSv2.43_packet/web/1000.pcap", 可以提取出类型/规则
        :param http_request: "33 44 55 66", 不太好提取了, 只能作为规则内容字段了
        :return: (catagory_id, request, response, attack, isvalid, from, module, cveid, sid, port, protocol, action), 即数据库所需的每个字段
        """
        result = re.findall(".*/([wafips]{3})v[0-9.]*_packet/([^/]*)/([0-9_]*).pcap", pcap_path, flags=re.IGNORECASE)[0]
        rule_type = result[0]
        sid = AutoTester.get_sid_from_pcap_name(pcap_path)
        encrypt_http_request = self.des_encrypt(http_request.encode("utf8"))

        # module 字段的值: WAF-3, IPS-2, PVS-4, APT 分表 默认是1
        module_id = self.get_module_id(rule_type)

        # 获取 catagory_id, 通过读取数据库对应记录的 attack_type 实现
        catagory_id = self.get_catagory_id(sid, rule_type)

        # isvalid 字段/action 字段默认为 1, Protocol 默认为 0
        return self.sample_http_obj(catagory_id, encrypt_http_request, "response", "attack",
                                    "1", "from", module_id, "cveid", sid, "80", "0", "1")

    def get_all_data_db_need(self, result_dict):
        """
        获取将要写入数据库的所有数据, 按照 wb 的要求:
        Catagory_id VARCHAR (10)
        Request TEXT
        Response TEXT
        Attack VARCHAR (1024)
        Isvalid BOOLEAN
        "From" VARCHAR (10)
        Module VARCHAR (8)
        CveID VARCHAR (128)
        Sid VARCHAR (32)
        Port INTEGER DEFAULT (80)
        Protocol INTEGER DEFAULT (0)
        "Action" INTEGER DEFAULT (1)
        :param result_dict: 自动化测试模块得到的 dict 数据, 可以从里面提取出规则/版本号等信息
        :return: list(), 每个元素都是命名元组, 包括数据库所需的各个字段
        """
        result_list = list()

        for pcap_path, http_request in result_dict.items():
            all_fields = self.get_all_fields(pcap_path, http_request)
            result_list.append(self.sample_http_obj(*all_fields))

        return result_list

    def run(self, db_path, table_name, af_mysql_info):
        """
        创建 lib 文件的整体流程
        :param db_path: str(), 目标 db 的路径
        :param af_mysql_info: 连接 af MySQL 所需的一切信息
        :param table_name: str(), 目标表名
        """
        # 创建 MySQL 连接, 查询 category_id 时要用到
        self.mysql = AFMySQLQuery(*af_mysql_info)

        # 创建 lib 文件
        self.create_sqlite_lib_file(db_path, table_name)

        # 关闭 MySQL 实体
        self.mysql.close_connect()

    def create_sqlite_lib_file(self, db_path, table_name):
        """
        创建 lib 文件
        :param db_path: str(), 目标 db 的路径
        :param table_name: str(), 目标表名
        """
        # 读取 json 数据, 解析为字典形式, 字典的键为规则 ID, 值为 HTTP 请求的十六进制流
        result_dict = self.format_json_file_to_hex_stream()

        # 提取每一个字段, 目前实现的字段:
        print("[*] 开始获取各个字段值以便写入数据库")
        all_data = self.get_all_data_db_need(result_dict)

        print("[*] 开始创建数据库并写入数据")
        with sqlite3.connect(db_path) as cursor:
            self.prepare_to_write_data_to_db(cursor, table_name)
            for each_row in all_data:
                self.insert_rule_to_db(cursor, table_name, each_row)
        print("[*] 数据库创建及写入完毕")

    @staticmethod
    def prepare_to_write_data_to_db(cursor, table_name):
        """
        准备好要写数据进数据库的环境搭建, 比如说创建数据库, 建表等
        :param cursor: 连接数据库的实例对象, 由 sqlite3.connect 产生
        :param table_name: 要处理的表名
        :return:
        """
        # 删除原来的表
        cursor.execute("DROP TABLE IF EXISTS {table_name}".format(table_name=table_name))

        # 重新创建表
        cursor.execute('CREATE TABLE {table_name} ('
                       'Id INTEGER PRIMARY KEY AUTOINCREMENT, '
                       'Catagory_id VARCHAR (10), '
                       'Request TEXT, Response TEXT, Attack VARCHAR (1024), '
                       'Isvalid BOOLEAN, "From" VARCHAR (10), Module VARCHAR (8), '
                       'CveID VARCHAR (128), Sid VARCHAR (32), Port INTEGER DEFAULT (80), '
                       'Protocol INTEGER DEFAULT (0), "Action" INTEGER DEFAULT (1));'.format(table_name=table_name))

        # 啥数据都没有
        result = cursor.execute("SELECT * FROM {table_name}".format(table_name=table_name))
        assert len(result.fetchall()) == 0

    @staticmethod
    def insert_rule_to_db(cursor, table_name, each_rule):
        """
        将规则插入数据库中
        :param cursor: 连接数据库的实例对象, 由 sqlite3.connect 产生
        :param table_name: str(), 表格名字
        :param each_rule: 命名元组, 内含所需的各个字段
        """
        # 插入数据
        insert_sql = "INSERT INTO {table_name} " \
                     "(Catagory_id,Request,Response,Attack,Isvalid,\"From\",Module,CveID,Sid,Port,Protocol,\"Action\") " \
                     "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)".format(table_name=table_name)

        result = cursor.execute(insert_sql, (
            each_rule.Catagory_id, each_rule.Request, each_rule.Response, each_rule.Attack,
            each_rule.Isvalid, each_rule.From, each_rule.Module, each_rule.CveID, each_rule.Sid, each_rule.Port,
            each_rule.Protocol, each_rule.Action))

        # 查看现有数据
        result = cursor.execute("SELECT * FROM {table_name}".format(table_name=table_name))
        result = result.fetchall()
        # 检查是否插入成功
        assert (len(result) > 0)


if __name__ == "__main__":
    af_mysql_information = ("192.192.90.134", "root", "root", "FW_LOG_fwlog")
    des_key = b"sangfor!"
    des_cbc_iv = b"sangfor*"
    lc = LibCreator(des_key, des_cbc_iv, "efficient_pcap.json")
    lc.run("test.lib", "aaa", af_mysql_information)
