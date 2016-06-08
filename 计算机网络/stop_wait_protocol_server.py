#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 计网大作业之一, 要求实现停等 ARQ 协议, 这是服务端, 负责收包

实现思路:
    建立一个服务端和客户端(具体实现时采用思路2):
        1. 用不可靠的 UDP 实现停等 ARQ 协议来实现可靠的传输
        2. 参考 spin 实验的思路, 通过模拟发送 err 或者 lost 等来模拟错误或丢失情况(TCP + 超时装饰器)
'''
# 要求如下:
# TODO: 能模拟 2 个终端进行数据通信，在通信过程中执行流控+差控协议的所有过程；
# TODO: 能模拟发送端和接收端的窗口滑动逻辑，即在窗口中的数据才能发送或者接收；
# TODO: 发送端、接收端的窗口大小可以自行设定；
# TODO: 数据帧编号为0~15
# TODO: 窗口滑动能可视化，即可以直观看到数据发送接收时窗口的滑动过程；
# TODO: 模拟通信可以用多种手段实现，例如进程间通信、socket、共享内存等
__author__ = '__L1n__w@tch'

import socketserver
import simplejson
import random

HOST, PORT = "localhost", 23337
# 模拟发包的类型
PACKET_TYPE = {"正常": "Message", "误码": "Error", "丢包": "Lost", "确认": "Ack", "否认": "Nak"}
MAX_FRAME_NUMBER = 15


class TCPHandler(socketserver.BaseRequestHandler):
    @staticmethod
    def receive_packet(sock):
        """
        负责用来收包的函数
        :param sock: 套接字
        :return: dict()
        """
        received_data = sock.recv(1024)
        received_data = simplejson.loads(received_data)

        return received_data

    @staticmethod
    def send_packet(sock, packet_type, seq, data_dict=dict()):
        """
        负责发包的函数
        :param sock: socket 套接字
        :param data_dict: 要发包的数据, 以字典形式表示
        :param seq: 接收到的包里面的区分号
        :return: flag, 用来表示是不是发了个丢失的包
        """
        flag = True

        # 模拟发包情况, 可能正常发包、发包误码、发的包丢失了
        data_dict["packet_type"] = random.choice(
            (PACKET_TYPE[packet_type], PACKET_TYPE["丢包"], PACKET_TYPE["误码"])
        )
        if data_dict["packet_type"] == PACKET_TYPE["丢包"]:
            # TODO: 这一部分写在超时重传里是不是好一些
            flag = False
        data_dict["send_seq"] = seq
        data = simplejson.dumps(data_dict)
        sock.sendall(data.encode("utf8"))

        return flag

    def handle(self):
        print("有客户端建立连接, 地址为: {}".format(self.client_address[0]))

        excepted_frame_number, excepted_seq = 0, 0

        while True:
            # 接收消息
            received_data = TCPHandler.receive_packet(self.request)

            # 收到正常消息
            if received_data["packet_type"] == PACKET_TYPE["正常"]:
                # 序号正常
                if received_data["send_seq"] == excepted_seq:
                    assert (excepted_frame_number == excepted_frame_number)
                    excepted_seq = 1 - excepted_seq
                    excepted_frame_number = (excepted_frame_number + 1) % MAX_FRAME_NUMBER

                    print("收到客户端发来的消息: {}".format(received_data))

                    # 回送 Ack
                    if not TCPHandler.send_packet(self.request, "确认", received_data["send_seq"]):
                        # 发包失败了, 进行两个恢复操作
                        excepted_seq = 1 - excepted_seq
                        excepted_frame_number = (excepted_frame_number + 1) % MAX_FRAME_NUMBER

                # 序号异常
                else:
                    TCPHandler.send_packet(self.request, "否认", received_data["send_seq"])

            elif received_data["packet_type"] == PACKET_TYPE["误码"]:
                # 收到误码消息
                # TODO: 模拟 ACK 误码或者 Nak 误码
                TCPHandler.send_packet(self.request, "否认", received_data["send_seq"])
            elif received_data["packet_type"] == PACKET_TYPE["丢包"]:
                # 收到丢失消息, 直接假装没收到就行了
                pass


if __name__ == "__main__":
    # 允许地址复用, 调试方便些
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer((HOST, PORT), TCPHandler)
    server.serve_forever()
