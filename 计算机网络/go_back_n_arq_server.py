#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 计网大作业之一, 要求实现:后退 N 帧 ARQ 协议, 这是服务端, 负责收包
'''
__author__ = '__L1n__w@tch'

import socketserver
import simplejson
import random
import bisect
import argparse

HOST, PORT = "localhost", 23339
# 模拟发包的类型
PACKET_TYPE = {"正常": "Message", "误码": "Error", "丢包": "Lost", "确认": "Ack"}
PROBABILITY = {"成功": 100, "误码": 0, "丢包": 0}  # 发包概率
MAX_FRAME_NUMBER = 16
RECEIVE_WINDOW_SIZE = 3
ACK_RETURN_NUMBER = RECEIVE_WINDOW_SIZE
VERBOSE = False  # 打印详细消息


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


class TCPHandler(socketserver.BaseRequestHandler):
    buffer_frame_pic = """
    {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}
    ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
    │{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│
    └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘"""

    def paint(self):
        """
        负责可视化的函数
        :return:
        """
        window_print = list()  # 用来画接收窗口的
        for i in range(MAX_FRAME_NUMBER + 1):
            if self.except_frame_number == i:
                window_print.append("\033[91m{}\033[0m".format("▛"))
            elif i == self.except_frame_number + self.receive_window_size:
                window_print.append("\033[91m{}\033[0m".format("▜"))
            # elif i == MAX_FRAME_NUMBER and \
            #                 (self.except_frame_number + self.receive_window_size) > MAX_FRAME_NUMBER:
            #     window_print.append("\033[91m{}\033[0m".format("▜"))
            else:
                window_print.append(" ")

        number_print = list()  # 用来表示帧号用的

        for i in range(MAX_FRAME_NUMBER):
            if i < self.except_frame_number:
                number_print.append(str(i).zfill(2))
            elif self.except_frame_number <= i < self.except_frame_number + self.receive_window_size:
                if i in self.received_buffer:
                    number_print.append("\033[91m{}\033[0m".format(str(i).zfill(2)))
                else:
                    number_print.append("\033[95m{}\033[0m".format(str(i).zfill(2)))
            else:
                number_print.append("  ")

        print(TCPHandler.buffer_frame_pic.format(*(window_print + number_print)))

    def receive_packet(self):
        """
        负责用来收包的函数
        :return: dict()
        """
        received_data = self.request.recv(1024)
        print("[{}] 收到包: {}".format(self.packet_counts, received_data), end="\n\n") if VERBOSE else None
        try:
            received_data = simplejson.loads(received_data)
        except simplejson.JSONDecodeError as e:
            print(received_data)
            raise RuntimeError("[*] 发生未知异常错误, 请试着降低发包速度")

        self.packet_counts += 1

        return received_data

    def send_packet(self, packet_type, frame_number):
        """
        负责发包的函数
        :param packet_type: 发包类型, 如"正常"
        :return:
        """
        data_dict = dict()

        # 模拟发包情况, 可能正常发包、发包误码、发的包丢失了
        data_dict["packet_type"] = weighted_choice([(PACKET_TYPE[packet_type], PROBABILITY["成功"]),
                                                    (PACKET_TYPE["误码"], PROBABILITY["误码"]),
                                                    (PACKET_TYPE["丢包"], PROBABILITY["丢包"])]
                                                   )
        data_dict["frame_number"] = frame_number

        data = simplejson.dumps(data_dict)
        self.request.sendall(data.encode("utf8").zfill(1024))  # 保证每次只拿到一个包
        self.packet_counts += 1
        print("[{}] 发送包: {}".format(self.packet_counts, data), end="\n\n") if VERBOSE else None

    def save_packet(self, frame_number):
        self.received_buffer.append(frame_number)

        self.paint()  # 可视化打印
        print("[*] 缓冲区中存在的包为: {}".format(self.received_buffer)) if VERBOSE else None
        # 滑动窗口
        if frame_number == self.except_frame_number:
            # 设置下一个希望收到的帧号
            self.set_next_except_frame_number()

        # 清空窗口中的缓冲区
        if len(self.received_buffer) >= MAX_FRAME_NUMBER:
            self.received_buffer.clear()
            self.first_cycle = False

    def is_except_packet(self, packet):
        """
        判断收到的包是否为接收窗口中希望收到的包
        :param packet: {"packet_type":"Message", "frame_number":0}
        :return: True or False
        """
        for i in range(self.receive_window_size):
            if packet["frame_number"] == (self.except_frame_number + i) % MAX_FRAME_NUMBER:
                return True
        return False

    def set_next_except_frame_number(self):
        """
        当收到重复帧时进行相关校验
        :return:
        """
        self.received_buffer = sorted(self.received_buffer)  # 进行排序

        # 判断下一个希望收到的帧号
        for i in range(len(self.received_buffer)):
            if i == len(self.received_buffer) - 1:
                if i == self.received_buffer[i]:
                    self.except_frame_number = (i + 1) % MAX_FRAME_NUMBER
                else:
                    self.except_frame_number = i
            elif i == self.received_buffer[i]:
                continue
            else:
                self.except_frame_number = i
                break

    def send_ack(self):
        """
        发送对应的确认帧号
        :return:
        """
        frame_number = (self.except_frame_number - 1) % MAX_FRAME_NUMBER
        if not self.first_cycle or frame_number != MAX_FRAME_NUMBER - 1:  # 第一轮循环就不回送帧 15 的 ack 了
            print("[!] 回送 Ack 包, 对帧 {} 进行确认".format(frame_number))
            print("[*] 回送 Ack {} 时, 缓冲区中存在的包为: {}".format(frame_number, self.received_buffer)) if VERBOSE else None
            self.send_packet("确认", frame_number)

    def initialize_variable(self):
        """
        初始化各种变量的
        :return:
        """
        self.first_cycle = True  # 判断是否是第一轮循环
        self.packet_counts = 0  # 用来计数收发包的数量
        self.received_buffer = list()  # 接收缓冲区
        self.receive_window_size = RECEIVE_WINDOW_SIZE  # 接收窗口大小
        self.except_frame_number = 0  # 期望收到的下一个帧号

    def get_current_window_frame_number(self):
        """
        计算当前接收窗口中的帧号
        :return:
        """
        _1, _2 = self.except_frame_number, (self.except_frame_number + self.receive_window_size - 1) % MAX_FRAME_NUMBER
        if _1 != _2:
            current_window_frame_number = "{}~{}".format(_1, _2)
        else:
            current_window_frame_number = "{}".format(_1)

        return current_window_frame_number

    def handle(self):
        self.initialize_variable()  # 初始化成员变量
        ack_counts = 0  # 用来计数用的, 计数值达到窗口大小时回送 Ack

        print("[*] 有客户端建立连接, 地址为: {}".format(self.client_address[0]))

        while True:
            received_data = self.receive_packet()  # 接收消息
            ack_counts += 1

            self.set_next_except_frame_number()
            if received_data["packet_type"] == PACKET_TYPE["正常"]:  # 收到正常消息
                if received_data["frame_number"] in self.received_buffer:
                    self.paint()  # 可视化打印
                    print("[?] 重复接收帧 {}".format(received_data["frame_number"]))

                elif self.is_except_packet(received_data):  # 是接收窗口中希望收到的帧号
                    # 保存帧
                    self.save_packet(received_data["frame_number"])

                    print("[?] 收到帧 {}".format(received_data["frame_number"]))

                else:  # 不是接收窗口中希望收到的帧号, 直接忽略
                    self.paint()  # 可视化打印
                    print("[?] 期望收到帧 {}, 但收到帧 {}".format(self.get_current_window_frame_number(),
                                                         received_data["frame_number"]))

            elif received_data["packet_type"] == PACKET_TYPE["误码"]:
                self.paint()  # 可视化打印
                print("[?] 收到的消息存在误码, 直接丢弃")  # 直接丢弃误码消息, 不回送 Nak
            elif received_data["packet_type"] == PACKET_TYPE["丢包"]:
                self.paint()  # 可视化打印
                print("[*] 什么都没收到")  # 收到丢失消息, 直接假装没收到就行了
            else:
                raise RuntimeError("[*] 收包异常")

            # 判断是否已经收到了指定数目的包, 是则回放 Ack
            if ack_counts == ACK_RETURN_NUMBER:
                self.send_ack()  # 回送对应的 Ack
                ack_counts = 0


def add_arguments(parser):
    parser.add_argument("--verbose", "-v", action="store_true", help="是否显示详细信息, 默认不显示")
    parser.add_argument("--probability", "-p", default="70:20:10", type=str,
                        help="设定发包概率, 格式:成功:误码:丢包, 默认值示例:70:20:10")
    parser.add_argument("--size", "-s", default=3, type=int, help="设定接收窗口大小, 默认值为 3")
    parser.add_argument("--ack", "-a", default=3, type=int,
                        help="设定大概多少个包以后回送 Ack, 默认与接收窗口大小相同, 建议该值≥发送窗口大小")


def set_arguments(opts):
    """
    用来将参数传递给全局变量的, 同时传递之前会进行安全检测
    :param parser: 解析器
    :param opts: 通过命令行获取的参数
    :return:
    """
    global VERBOSE, PROBABILITY, RECEIVE_WINDOW_SIZE, ACK_RETURN_NUMBER

    VERBOSE = opts.verbose

    _1, _2, _3 = [int(x) for x in opts.probability.split(":")]
    if _1 + _2 + _3 == 100:
        PROBABILITY["成功"], PROBABILITY["误码"], PROBABILITY["丢包"] = _1, _2, _3
    else:
        print("概率参数设置错误, 将采取默认值-70:20:10")

    if 0 < opts.size < MAX_FRAME_NUMBER:
        RECEIVE_WINDOW_SIZE = opts.size
    else:
        print("[*] 窗口大小参数错误, 采取默认值 3")
        RECEIVE_WINDOW_SIZE = 3

    if 0 < opts.ack < MAX_FRAME_NUMBER:
        ACK_RETURN_NUMBER = opts.ack
    else:
        print("[*] Ack 参数错误, 采取默认值, 与接收窗口大小相同")
        ACK_RETURN_NUMBER = RECEIVE_WINDOW_SIZE


if __name__ == "__main__":
    # 处理命令行参数
    parser = argparse.ArgumentParser(description="回退 N 帧 ARQ 协议-服务端")
    add_arguments(parser)
    opts = parser.parse_args()
    set_arguments(opts)

    # 允许地址复用, 调试方便些
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer((HOST, PORT), TCPHandler)

    print("""
         ◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎
         ◎           Server           ◎
         ◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎◎""")
    print("服务端准备完毕...") if VERBOSE else None
    server.serve_forever()
