#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 计网大作业之一, 要求实现:后退 N 帧 ARQ 协议, 这是客户端, 负责发包

具体要求：
    Done: 要求能模拟2个终端进行数据通信，在通信过程中执行流控+差控协议的所有过程；
    Done: 要求能模拟发送端和接收端的窗口滑动逻辑，即在窗口中的数据才能发送或者接收；
    Done: 要求发送端、接收端的窗口大小可以自行设定；
    Done: 要求数据帧编号为0~15；
    Done: 要求窗口滑动能可视化，即可以直观看到数据发送接收时窗口的滑动过程；
    Done: 模拟通信可以用多种手段实现，例如进程间通信、socket、共享内存等；
"""
import socket
import simplejson
import random
import bisect
import time
import argparse

__author__ = '__L1n__w@tch'

HOST, PORT = "localhost", 23339
# 模拟发包的类型
PACKET_TYPE = {"正常": "Message", "误码": "Error", "丢包": "Lost", "确认": "Ack"}
PROBABILITY = {"成功": 100, "误码": 0, "丢包": 0}  # 发包概率
MAX_FRAME_NUMBER = 16
TIMEOUT = 2
SEND_WINDOW_SIZE = 3
VERBOSE = False  # 是否打印详细信息


def weighted_choice(choices):
    """
    带权随机选择函数
    :param choices: [("WHITE", 60), ("RED", 30), ("GREEN", 10)]
    :return: "WHITE"
    """
    values, weights = zip(*choices)
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random.random() * total
    i = bisect.bisect(cum_weights, x)
    return values[i]


class Sender:
    buffer_frame_pic = """
    {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}
    ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
    │{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│
    └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘"""

    def __init__(self, sock2server):
        self.sock = sock2server
        self.frame_number = 0
        self.packet_counts = 0  # 用来计数收发包的数量
        self.window_size = SEND_WINDOW_SIZE  # 发送窗口大小

    def paint(self):
        """
        负责画图的函数
        :return:
        """
        window_print = list()  # 用来画接收窗口的
        for i in range(MAX_FRAME_NUMBER + 1):
            if self.frame_number == i:
                window_print.append("\033[91m{}\033[0m".format("▛"))
            elif i == self.frame_number + self.window_size:
                window_print.append("\033[91m{}\033[0m".format("▜"))
            else:
                window_print.append(" ")

        number_print = list()

        for i in range(MAX_FRAME_NUMBER):
            if i < self.frame_number - 1:
                number_print.append("√ ")
            elif i == self.frame_number - 1:
                number_print.append("\033[91m{}\033[0m".format("√ "))
            elif self.frame_number <= i < self.frame_number + self.window_size:
                number_print.append("\033[95m{}\033[0m".format(str(i).zfill(2)))
            else:
                number_print.append(str(i).zfill(2))

        print(Sender.buffer_frame_pic.format(*(window_print + number_print)))

    def send_window_data(self, start_frame_number):
        """
        将发送窗口中的帧发送出去
        :param start_frame_number: 从第几号帧开始发送
        :return:
        """
        for i in range(self.window_size):
            send_frame_number = (start_frame_number + i) % MAX_FRAME_NUMBER
            print("[!] 发送帧 {}".format(send_frame_number)) if VERBOSE else None
            self.send_packet("正常", send_frame_number)
            time.sleep(TIMEOUT)

    def send_packet(self, packet_type, frame_number):
        """
        发送单个帧
        :param packet_type: 发帧类型(其实发送端只会发送正常包)
        :param frame_number: 帧号
        :return:
        """
        data_dict = dict()
        data_dict["frame_number"] = frame_number
        # 模拟发包情况, 可能正常发包、发包误码、发的包丢失了
        data_dict["packet_type"] = weighted_choice([(PACKET_TYPE[packet_type], PROBABILITY["成功"]),
                                                    (PACKET_TYPE["误码"], PROBABILITY["误码"]),
                                                    (PACKET_TYPE["丢包"], PROBABILITY["丢包"])]
                                                   )

        data = simplejson.dumps(data_dict)
        sock.sendall(data.encode("utf8"))
        self.packet_counts += 1
        print("[{}] 发送包: {}".format(self.packet_counts, data), end="\n\n") if VERBOSE is True else None

    def receive_packet(self):
        """
        负责用来收包的函数
        :return: dict()
        """
        sock.settimeout(TIMEOUT * 2.5)
        received_data = self.sock.recv(1024).strip(b"0")  # 保证每次只拿到一个包
        print("[{}] 收到包: {}".format(self.packet_counts, received_data), end="\n\n") if VERBOSE is True else None
        received_data = simplejson.loads(received_data)
        self.packet_counts += 1

        return received_data

    def get_current_window_frame_number(self):
        """
        计算当前发送窗口中的帧号
        :return:
        """
        _1, _2 = self.frame_number, (self.frame_number + self.window_size - 1) % MAX_FRAME_NUMBER
        if _1 != _2:
            current_window_frame_number = "{}~{}".format(_1, _2)
        else:
            current_window_frame_number = "{}".format(_1)

        return current_window_frame_number

    def cycle_send(self):
        """
        负责循环发包的函数
        :return:
        """
        print("[*] 连接上服务端了") if VERBOSE else None

        # 将发送窗口中的帧发送出去
        self.paint()
        print("[!] 开始发送消息, 发送帧 {}".format(self.get_current_window_frame_number()))
        self.send_window_data(self.frame_number)
        while True:
            try:  # 超时重传控制
                received_data = self.receive_packet()
            except socket.timeout:
                self.paint()  # 可视化打印
                print("[*] 超时重传; [!] 发送帧{}".format(self.get_current_window_frame_number()))
                self.send_window_data(self.frame_number)  # 将发送窗口中的帧发送出去
                continue

            if received_data["packet_type"] == PACKET_TYPE["确认"]:  # 收到 Ack 确认
                self.frame_number = (int(received_data["frame_number"]) + 1) % MAX_FRAME_NUMBER  # 产生帧编号

                self.paint()  # 可视化打印
                print("[?] 收到帧 {} 的 Ack 应答包; [!] 发送帧{}".format(received_data["frame_number"],
                                                               self.get_current_window_frame_number()))
                self.send_window_data(self.frame_number)  # 发送接下来的帧

            elif received_data["packet_type"] == PACKET_TYPE["丢包"]:
                self.paint()  # 可视化打印
                print("[*] 什么都没收到")  # 收到丢失消息, 直接假装没收到就行了

            elif received_data["packet_type"] == PACKET_TYPE["误码"]:
                self.paint()  # 可视化打印
                print("[?] 收到误码包; [!] 重发帧 {}".format(self.get_current_window_frame_number()))
                self.send_window_data(self.frame_number)  # 将发送窗口中的帧发送出去
            else:
                raise RuntimeError("[*] 收包不正常")


def add_arguments(arg_parser):
    arg_parser.add_argument("--verbose", "-v", action="store_true", help="是否显示详细信息, 默认不显示")
    arg_parser.add_argument("--probability", "-p", default="70:20:10", type=str,
                            help="设定发包概率, 格式:成功:误码:丢包, 默认值示例:70:20:10")
    arg_parser.add_argument("--size", "-s", default=3, type=int, help="设定接收窗口大小, 默认值为 3")
    arg_parser.add_argument("--timeout", "-t", default=2, type=float,
                            help="设置时延, 发包间隔 TIMEOUT 秒, 超时等待 TIMEOUT * 2.5 秒. 默认值为 2.0")


def set_arguments(options):
    """
    用来将参数传递给全局变量的, 同时传递之前会进行安全检测
    :param options: 通过命令行获取的参数
    :return:
    """
    global VERBOSE, PROBABILITY, SEND_WINDOW_SIZE, TIMEOUT

    VERBOSE = options.verbose

    _1, _2, _3 = [int(x) for x in options.probability.split(":")]
    if _1 + _2 + _3 == 100:
        PROBABILITY["成功"], PROBABILITY["误码"], PROBABILITY["丢包"] = _1, _2, _3
    else:
        print("概率参数设置错误, 将采取默认值-70:20:10")

    if 0 < options.size < MAX_FRAME_NUMBER:
        SEND_WINDOW_SIZE = options.size
    else:
        print("[*] 窗口大小参数错误, 采取默认值 3")
        SEND_WINDOW_SIZE = 3

    TIMEOUT = options.timeout


if __name__ == "__main__":
    # 处理命令行参数
    parser = argparse.ArgumentParser(description="""回退 N 帧 ARQ 协议-客户端""")
    add_arguments(parser)
    opts = parser.parse_args()
    set_arguments(opts)

    print("""
         ◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎
         ◎           Client           ◎
         ◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎""")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))

        sender = Sender(sock)
        # 循环发帧给服务端的函数
        sender.cycle_send()
    finally:
        sock.close()
