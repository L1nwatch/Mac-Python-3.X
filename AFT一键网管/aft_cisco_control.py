#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.13 决定不写 UI 界面了， 直接上终端交互吧，回头采用 B/S 架构
2017.01.08 尝试 telnet
"""
import telnetlib
import re
import os
import subprocess
from collections import namedtuple

__author__ = '__L1n__w@tch'


class AFTCiscoControl:
    def __init__(self, ip_address):
        """
        初始化
        :param ip_address: 目标 telnet 服务端的 IP
        """
        # 连接Telnet服务器
        self.tn = telnetlib.Telnet(ip_address)  # 连接设备的实例
        self.in_out = namedtuple("in_out", ["In", "Out"])

    @staticmethod
    def block_read_information_from_telnet(tn):
        """
        从 tn 读取信息, 注意这方法必定会陷入死循环，这个只是用来调试用的
        :param tn: telnet.lib.Telnet() 的返回值
        """

        data = tn.read_some()
        while len(data) > 0:
            print(data.decode("gbk"), end="")
            data = tn.read_some()

    @staticmethod
    def get_telnet_server_os(tn):
        """
        判断 telnet 服务端操作系统
        :param tn: 获取 telnet 服务端的操作系统类型
        :return: str(), 比如 "Darwin"(mac)
        """
        # TODO: 这个方法还没有实现
        return "Others"

    def send_data_to_telnet_server(self, message):
        """
        发送数据给 telnet 服务端, 会自动补全换行符
        :param message: str(), 待发送的消息
        """
        os = self.get_telnet_server_os(self.tn)
        if "Win" == os:
            self.tn.write("{}\r\n".format(message).encode("gbk"))
        else:
            self.tn.write("{}\n".format(message).encode("utf8"))

    def telnet_login(self, tn, user_name, password):
        """
        完成登录操作
        :param tn: <class 'telnetlib.Telnet'>
        :param user_name: str(), 用户名, 如 "watch"
        :param password: str(), 密码, 如 "watch"
        """
        # 输入登录用户名
        tn.read_until(b'login: ')
        self.send_data_to_telnet_server(tn, user_name)

        # 输入登录密码
        tn.read_until(b'password: ')
        self.send_data_to_telnet_server(tn, password)

        # 登录完毕后，执行ls命令
        tn.read_until("{}>".format(user_name).encode("utf8"))

    def connect_core_switch_device(self, password):
        """
        telnet 进核心交换机
        :param password: str(), 密码, 如 "watch"
        """
        # 登录认证
        print("[*] 尝试进行登陆操作")
        self.tn.read_until(b"Password:")
        self.send_data_to_telnet_server(password)

        # 进入特权模式
        print("[*] 尝试进入特权模式")
        self.tn.read_until(b"AF>")
        self.send_data_to_telnet_server("enable")
        self.tn.read_until(b"Password")
        self.send_data_to_telnet_server(password)

        self.tn.read_until(b"AF#")
        print("[*] 进入特权模式完毕，可以执行命令了")

    def close_connect(self):
        if self.tn:
            # ls命令执行完毕后，终止Telnet连接（或输入exit退出）
            self.tn.close()  # tn.write('exit\n')
            print("[*] 关闭连接成功")
        else:
            print("[!] 不存在连接")

    def read_one_line(self):
        """
        读取一行数据
        :return: str(), 一行数据
        """
        result = self.tn.read_until(b"\n")
        return result

    def get_pointed_fast_in_out_packet_number(self):
        """
        获取指定接口的进出口流量信息
        :return:
        """
        self.send_data_to_telnet_server(" ")
        result = self.tn.read_until(b"AF#\r\n")
        result = self.extract_inout_information(result)
        return self.in_out(*result)

    def get_show_interfaces_counters_result(self):
        """
        执行 show interfaces counters  命令， 获取结果并打印
        :return: byte(), 执行命令的结果
        """
        print("[*] 执行命令：{}".format("show interfaces counters"))
        self.send_data_to_telnet_server("show interfaces counters")
        self.send_data_to_telnet_server(" ")
        result = self.tn.read_until(b"AF#")
        print(result.decode("utf8"))
        return result

    def get_all_in_out_stream_information(self, ignore_zero=False):
        """
        获取所有接口的进出流量信息
        :param ignore_zero: True or False, 决定是否忽略 0 流量口的信息
        :return: dict(), {1: (21, 256), 2: (800, 1201), 3: (0, 0), 4: (0, 0), ... }
        """
        result_dict = dict()

        print("[*] 开始读取所有接口的进出流量信息，是否选择忽略 0 流量口信息：{}".format(ignore_zero))
        for i in range(1, 25):
            # 发送指令，获取 i 口情况
            self.send_data_to_telnet_server("show interfaces fastEthernet 0/{}".format(i))

            # 获取进出流量
            result = self.get_pointed_fast_in_out_packet_number()
            if not ignore_zero or int(result.In) != 0 or int(result.Out) != 0:
                print("[*] 读取 {} 口流量信息，In = {}，Out = {}".format(i, result.In.decode("utf8"), result.Out.decode("utf8")))

            # 保存结果到字典中
            result_dict[i] = (int(result.In), int(result.Out))

        return result_dict

    @staticmethod
    def extract_inout_information(data):
        """
        从信息流中提取出进出口流量信息
        :param data:  b'show  interfaces fastEthernet 0/1\r\nFastEthernet0/1 is up, line protocol ...'
        :return: (b"18", b"325")
        """
        result = re.findall(
            b"5 minute input rate \d* bits/sec, (\d*) packets/sec\r\n  5 minute output rate \d* bits/sec, (\d*) packets/sec\r\n",
            data, flags=re.IGNORECASE)[0]
        return result[0], result[1]

    def config_t_interfaces(self, number, command):
        """
        关闭某个口
        :param number: int, 表明要关闭哪个口
        :param command: str(), 要执行的命令
        :return: None
        """
        assert 1 <= number <= 24
        self.send_data_to_telnet_server("config t")
        self.tn.read_until(b"AF(config)#")
        print("[*] 进入 config 模式")

        self.send_data_to_telnet_server("interface fastEthernet 0/{}".format(number))
        self.tn.read_until(b"AF(config-if)#")
        print("[*] 进入 {} 口的 config-if 模式".format(number))

        print("[*] 开始执行命令 {}".format(command))
        self.send_data_to_telnet_server(command)
        self.tn.read_until(b"AF(config-if)#")
        print("[*] 命令执行成功".format(number))

        self.send_data_to_telnet_server("exit")
        self.tn.read_until(b"AF(config)#")
        self.send_data_to_telnet_server("exit")
        self.tn.read_until(b"AF#")
        print("[*] 退出 config、config-t 模式")


def execute_ping_command(target_ip):
    """
    执行 ping 命令
    :param target_ip: str(), 目标 IP 地址
    :return: byte(), 命令执行结果
    """
    with subprocess.Popen("ping {} -n 5".format(target_ip), stdout=subprocess.PIPE, shell=True) as proc:
        res = proc.stdout.read()
    print(res)
    print(res.decode("gbk"))
    return res


if __name__ == "__main__":
    # execute_ping_command("200.200.0.33")
    # exit(0)

    # 配置选项
    ip = '155.155.155.25'  # Telnet服务器IP
    telnet_password = 'sangfor'  # 登录密码

    tc = AFTCiscoControl(ip)
    tc.connect_core_switch_device(telnet_password)
    result = tc.get_all_in_out_stream_information(ignore_zero=True)
    # tc.get_show_interfaces_counters_result()
    # tc.config_t_interfaces(16, "shutdown")
    tc.close_connect()
