#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.08 尝试 telnet
"""
import telnetlib

__author__ = '__L1n__w@tch'


class TelnetConnect:
    def __init__(self, telnet_server_ip, user_name, password):
        self.telnet_server_ip = telnet_server_ip
        self.user_name = user_name
        self.password = password
        self.telnet_server_os = None    # telnet 服务端操作系统类型

    def read_information_from_telnet(tn):
        """
        从 tn 读取信息, 注意这会陷入死循环直到超时
        :param tn: telnet.lib.Telnet() 的返回值
        """

        data = tn.read_some()
        while len(data) > 0:
            print(data.decode("gb2312"), end="")
            data = tn.read_some()

    def get_telnet_server_os(tn):
        """
        判断 telnet 服务端操作系统
        :param tn: 获取 telnet 服务端的操作系统类型
        :return: str(), 比如 "Darwin"(mac)
        """
        data = tn.read_some().lower()
        if b"microsoft" in data:
            return "Win"
        elif b"linux" in data:
            return "Linux"
        else:
            return "Others"

    def send_data_to_telnet_server(tn, message):
        """
        发送数据给 telnet 服务端, 会自动补全换行符
        :param tn: <class 'telnetlib.Telnet'>
        :param message: 待发送的消息
        """
        os = get_telnet_server_os()
        if "Win" == os:
            tn.write("{}\r\n".format(message).encode("gbk"))
        else:
            tn.write("{}\n".format(message).encode("utf8"))

    def telnet_login(tn, user_name, password):
        """
        完成登录操作
        :param user_name: str(), 用户名, 如 "watch"
        :param password: str(), 密码, 如 "watch"
        """
        # 输入登录用户名
        tn.read_until(b'login: ')
        send_data_to_telnet_server(tn, user_name)

        # 输入登录密码
        tn.read_until(b'password: ')
        send_data_to_telnet_server(tn, password)

        # 登录完毕后，执行ls命令
        tn.read_until(finish.encode("utf8"))

    def telnet_connect(ip_address, user_name, password, finish):
        """
        进行 telnet 连接
        :param ip_address: str(), 目标 IP 地址, 如 "192.168.158.130"
        :param user_name: str(), 用户名, 如 "watch"
        :param password: str(), 密码, 如 "watch"
        :param finish: str(), 命令提示符（标识着上一条命令已执行完毕）, 如 "watch>"
        """
        # 连接Telnet服务器
        tn = telnetlib.Telnet(ip)
        telnet_server_os = get_telnet_server_os(tn)
        print(telnet_server_os)

        telnet_login(tn, user_name, password)
        send_data_to_telnet_server(tn, "dir")

        read_information_from_telnet(tn)

        # ls命令执行完毕后，终止Telnet连接（或输入exit退出）
        tn.read_until(finish)
        tn.close()  # tn.write('exit\n')


if __name__ == "__main__":
    # 配置选项
    ip = '192.168.158.130'  # Telnet服务器IP
    username = 'watch'  # 登录用户名
    password = 'watch'  # 登录密码
    finish = 'watch>'   # 登录结束标志

    tc = TelnetConnect(ip, username, password)
