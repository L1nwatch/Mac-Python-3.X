#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 计网大作业之一, 要求实现停等 ARQ 协议, 这是客户端, 负责发包
'''
__author__ = '__L1n__w@tch'

import socket
import simplejson
import time
import random

HOST, PORT = "localhost", 23337
# 模拟发包的类型
PACKET_TYPE = {"正常": "Message", "误码": "Error", "丢包": "Lost", "确认": "Ack", "否认": "Nak"}
MAX_FRAME_NUMBER = 15
TIMEOUT = 1  # 每隔 1 s 发送一个包


def send_packet(sock, data_dict, frame_number):
    """
    负责发包的函数
    :param sock: socket 套接字
    :param data_dict: 要发包的数据, 以字典形式表示
    :param frame_number: 要发送的包的帧编号
    :return:
    """
    # 产生帧编号
    data_dict["frame_number"] = (frame_number + 1) % MAX_FRAME_NUMBER
    # 模拟发包情况, 可能正常发包、发包误码、发的包丢失了
    data_dict["packet_type"] = random.choice(
        (PACKET_TYPE["正常"], PACKET_TYPE["误码"], PACKET_TYPE["丢包"])
    )
    data = simplejson.dumps(data_dict)
    sock.sendall(data.encode("utf8"))


def receive_packet(sock):
    """
    负责用来收包的函数
    :param sock: 套接字
    :return: dict()
    """
    received_data = sock.recv(1024)
    received_data = simplejson.loads(received_data)

    return received_data


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))

        frame_number, send_seq = MAX_FRAME_NUMBER - 1, 0  # send_seq 作为区分号
        data_dict = {"send_seq": send_seq}

        while True:
            time.sleep(TIMEOUT)  # 控制发包速度

            # 发包
            send_packet(sock, data_dict, frame_number)

            # TODO: 超时重传
            # 期望收到对方发来 Ack 确认
            received_data = receive_packet(sock)

            # 收到 Ack 确认
            if received_data["packet_type"] == PACKET_TYPE["确认"]:
                # 收到 Ack 应答, 且序号正确, 则发送下一个包
                if received_data["send_seq"] == send_seq:
                    # 产生下一个包的区分号和帧号
                    data_dict["send_seq"] = 1 - send_seq
                    frame_number += 1

                # 收到 Ack 应答, 但是序号不对, 重新发包
                else:
                    send_packet(sock, data_dict, frame_number)
            # 收到丢失消息, 直接假装没收到就行了
            elif received_data["packet_type"] == PACKET_TYPE["丢包"]:
                pass
            # 发包误码, 重新发包
            elif received_data["packet_type"] == PACKET_TYPE["误码"]:
                send_packet(sock, data_dict, frame_number)
            # 发的包不正确, 重新发包
            elif received_data["packet_type"] == PACKET_TYPE["否认"]:
                send_packet(sock, data_dict, frame_number)
            else:
                raise RuntimeError("[?] 收包不正常")
    finally:
        sock.close()
