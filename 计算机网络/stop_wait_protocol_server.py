#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 计网大作业之一, 要求实现停等 ARQ 协议, 这是服务端, 负责收包

实现思路:
    建立一个服务端和客户端(具体实现时采用思路2):
        1. 用不可靠的 UDP 实现停等 ARQ 协议来实现可靠的传输
        2. 参考 spin 实验的思路, 通过模拟发送 err 或者 lost 等来模拟错误或丢失情况
"""
# 要求如下:
# Done: 能模拟 2 个终端进行数据通信，在通信过程中执行流控+差控协议的所有过程；
# Done: 能模拟发送端和接收端的窗口滑动逻辑，即在窗口中的数据才能发送或者接收；
# No: 发送端、接收端的窗口大小可以自行设定；(停等 ARQ 协议就不需要这个功能了吧, 才收发 1 个包)
# Done: 数据帧编号为0~15
# Done: 窗口滑动能可视化，即可以直观看到数据发送接收时窗口的滑动过程；
# Done: 模拟通信可以用多种手段实现，例如进程间通信、socket、共享内存等
import socketserver
import simplejson
import random
import bisect
import argparse

__author__ = '__L1n__w@tch'

HOST, PORT = "localhost", 23337
# 模拟发包的类型
PACKET_TYPE = {"正常": "Message", "误码": "Error", "丢包": "Lost", "确认": "Ack", "否认": "Nak"}
PROBABILITY = {"成功": 70, "误码": 20, "丢包": 10}
MAX_FRAME_NUMBER = 16
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


class TCPHandler(socketserver.BaseRequestHandler):
    buffer_frame_pic = """

    ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
    │{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│
    └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘"""

    def paint(self):
        """
        负责可视化的函数, 同时也负责收到最后一个帧时清空缓冲区
        :return:
        """
        for_print = list()

        for i in range(MAX_FRAME_NUMBER):
            if i < len(self.received_buffer) - 1:
                for_print.append(str(i).zfill(2))
            elif i == len(self.received_buffer) - 1:
                for_print.append("\033[91m{}\033[0m".format(str(i).zfill(2)))
            else:
                for_print.append("  ")

        print(TCPHandler.buffer_frame_pic.format(*for_print))

        if len(self.received_buffer) == MAX_FRAME_NUMBER:
            self.received_buffer.clear()

    def receive_packet(self, sock):
        """
        负责用来收包的函数
        :param sock: 套接字
        :return: dict()
        """
        received_data = sock.recv(1024)
        received_data = simplejson.loads(received_data)

        self.packet_counts += 1
        print("[{}] 收到包: {}".format(self.packet_counts, received_data), end="\n\n") if VERBOSE is True else None

        return received_data

    def send_packet(self, sock, packet_type, seq):
        """
        负责发包的函数
        :param sock: socket 套接字
        :param packet_type: 发包类型
        :param seq: 接收到的包里面的区分号
        :return: flag, 用来表示是不是发了个丢失的包
        """
        data_dict = dict()

        data_dict["send_seq"] = seq
        # 模拟发包情况, 可能正常发包、发包误码、发的包丢失了
        data_dict["packet_type"] = weighted_choice([(PACKET_TYPE[packet_type], PROBABILITY["成功"]),
                                                    (PACKET_TYPE["误码"], PROBABILITY["误码"]),
                                                    (PACKET_TYPE["丢包"], PROBABILITY["丢包"])]
                                                   )

        data = simplejson.dumps(data_dict)
        sock.sendall(data.encode("utf8"))
        self.packet_counts += 1
        print("[{}] 发送包: {}".format(self.packet_counts, data), end="\n\n") if VERBOSE is True else None

    def save_packet(self, frame_number):
        self.last_frame_number = frame_number  # 保存正常收包的最后一个帧号
        self.received_buffer.append(frame_number)

    def handle(self):
        self.packet_counts = 0  # 包的计数器
        excepted_frame_number, excepted_seq = 0, 0
        self.received_buffer, self.last_frame_number = list(), -1
        print("[*] 有客户端建立连接, 地址为: {}".format(self.client_address[0]))

        while True:
            received_data = self.receive_packet(self.request)  # 接收消息

            if received_data["packet_type"] == PACKET_TYPE["正常"]:  # 收到正常消息
                if received_data["send_seq"] == excepted_seq:  # 序号正常
                    assert (excepted_frame_number == excepted_frame_number)  # TODO: 如果帧号不一致的情况呢?

                    self.save_packet(excepted_frame_number)  # 保存相应的包
                    self.paint()  # 可视化表示收包
                    print("[?] 收到帧号为 {} 的消息, 区分号为 {}; [!] 回送 Ack 包".format(excepted_frame_number, excepted_seq))

                    excepted_seq = 1 - excepted_seq  # 产生下一帧的区分号
                    excepted_frame_number = (excepted_frame_number + 1) % MAX_FRAME_NUMBER  # 产生下一帧的帧号
                    self.send_packet(self.request, "确认", received_data["send_seq"])  # 回送 Ack

                else:  # 序号异常
                    if received_data["frame_number"] == self.last_frame_number:  # 已经收过的包
                        self.send_packet(self.request, "确认", received_data["send_seq"])  # 不保存, 回发 Ack 包
                    else:
                        self.paint()  # 可视化表示收包
                        print("[?] 收到帧号为 {} 的消息, 区分号为 {}, 期望收到帧号为 {} 的消息, 区分号为 {}; "
                              "[!] 回送 Nak 包".format(received_data["frame_number"], received_data["send_seq"],
                                                    excepted_frame_number, excepted_seq))
                        self.send_packet(self.request, "否认", received_data["send_seq"])

            elif received_data["packet_type"] == PACKET_TYPE["误码"]:  # 收到误码消息
                self.paint()  # 可视化表示收包
                print("[?] 收到的消息存在误码; [!] 回送 Nak 包")
                self.send_packet(self.request, "否认", received_data["send_seq"])
            elif received_data["packet_type"] == PACKET_TYPE["丢包"]:
                self.paint()  # 可视化表示收包
                print("[*] 什么都没收到")  # 收到丢失消息, 直接假装没收到就行了


def add_arguments(arg_parser):
    arg_parser.add_argument("--verbose", "-v", action="store_true", help="是否显示详细信息, 默认不显示")
    arg_parser.add_argument("--probability", "-p", default="70:20:10", type=str,
                            help="设定发包概率, 格式:成功:误码:丢包, 默认值示例:70:20:10")


def set_arguments(options):
    global VERBOSE, PROBABILITY

    VERBOSE = options.verbose
    _1, _2, _3 = [int(x) for x in options.probability.split(":")]
    if _1 + _2 + _3 == 100:
        PROBABILITY["成功"], PROBABILITY["误码"], PROBABILITY["丢包"] = _1, _2, _3
    else:
        print("概率参数设置错误, 将采取默认值-70:20:10")


if __name__ == "__main__":
    # 处理命令行参数
    parser = argparse.ArgumentParser(description="停等 ARQ 协议-服务端")
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
    if VERBOSE is True:
        print("服务端准备完毕...")
    server.serve_forever()
