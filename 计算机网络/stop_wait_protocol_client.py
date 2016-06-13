#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 计网大作业之一, 要求实现停等 ARQ 协议, 这是客户端, 负责发包

Funny: 本来想用超时检测器的, 发现一旦出现超时 socket 就不正常工作了, 所以还是直接用 socket 的 settimeout 算了...
"""
import socket
import simplejson
import time
import random
import bisect
import argparse

__author__ = '__L1n__w@tch'

HOST, PORT = "127.0.0.1", 23337
# 模拟发包的类型
PACKET_TYPE = {"正常": "Message", "误码": "Error", "丢包": "Lost", "确认": "Ack", "否认": "Nak"}
PROBABILITY = {"成功": 70, "误码": 20, "丢包": 10}
MAX_FRAME_NUMBER = 16
TIMEOUT = 2  # 每隔 TIMEOUT s 发送一个包
packet_counts = 0  # 包的计数器
VERBOSE = False  # 是否打印详细信息


def paint(frame_number):
    """
    负责画图的函数
    :param frame_number: 已经确认发送成功的帧号
    :return:
    """
    buffer_frame_pic = """

    ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
    │{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│
    └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘"""

    buffer = list()

    for i in range(MAX_FRAME_NUMBER):
        if i < frame_number - 1:
            buffer.append("√ ")
        elif i == frame_number - 1:
            buffer.append("\033[91m{}\033[0m".format("√ "))
        elif i == frame_number:
            buffer.append("\033[95m{}\033[0m".format(str(i).zfill(2)))
        else:
            buffer.append(str(i).zfill(2))

    print(buffer_frame_pic.format(*buffer))


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


def send_packet(sock2server, seq, frame_number, packet_type):
    """
    负责发包的函数
    :param sock2server: 套接字
    :param seq: 区分号, 0 或 1
    :param frame_number: 帧编号
    :param packet_type: 发包类型
    :return:
    """
    global packet_counts

    data_dict = dict()
    data_dict["send_seq"] = seq
    data_dict["frame_number"] = frame_number
    # 模拟发包情况, 可能正常发包、发包误码、发的包丢失了
    data_dict["packet_type"] = weighted_choice([(PACKET_TYPE[packet_type], PROBABILITY["成功"]),
                                                (PACKET_TYPE["误码"], PROBABILITY["误码"]),
                                                (PACKET_TYPE["丢包"], PROBABILITY["丢包"])]
                                               )

    data = simplejson.dumps(data_dict)
    sock2server.sendall(data.encode("utf8"))
    packet_counts += 1
    print("[{}] 发送包: {}".format(packet_counts, data), end="\n\n") if VERBOSE is True else None


def receive_packet(sock2server):
    """
    负责用来收包的函数
    :param sock2server: 套接字
    :return: dict()
    """
    global packet_counts

    sock2server.settimeout(TIMEOUT * 2.5)
    received_data = sock2server.recv(1024)
    received_data = simplejson.loads(received_data)
    packet_counts += 1
    print("[{}] 收到包: {}".format(packet_counts, received_data), end="\n\n") if VERBOSE is True else None

    return received_data


def cycle_send(sock2server):
    """
    循环给服务端发送帧 0~15
    :param sock2server: 套接字
    :return:
    """
    frame_number, seq = 0, 0  # send_seq 作为区分号
    # 发第一帧
    paint(frame_number)  # 可视化发送窗口
    print("[!] 开始发送消息, 发送帧{}".format(frame_number))
    send_packet(sock2server, seq, frame_number, "正常")
    while True:
        time.sleep(TIMEOUT)  # 控制程序执行速度

        try:  # 超时重传控制
            received_data = receive_packet(sock2server)
        except socket.timeout:
            paint(frame_number)  # 可视化发送窗口
            print("[*] 超时重传; [!] 发送帧{}".format(frame_number))
            send_packet(sock2server, seq, frame_number, "正常")
            continue

        if received_data["packet_type"] == PACKET_TYPE["确认"]:  # 收到 Ack 确认
            if received_data["send_seq"] == seq:  # 收到 Ack 应答, 且序号正确, 则发送下一个包
                seq = 1 - seq  # 产生下一个包的区分号和帧号
                frame_number = (frame_number + 1) % MAX_FRAME_NUMBER  # 产生帧编号
                paint(frame_number)  # 可视化发送窗口
                print("[?] 收到 Ack 应答包, 且区分号正确; [!] 发送下一帧{}".format(frame_number))
                send_packet(sock2server, seq, frame_number, "正常")  # 发送下一个包

            else:  # 收到 Ack 应答, 但是序号不对, 重新发包
                paint(frame_number)  # 可视化发送窗口
                print("[?] 收到 Ack 应答包, 但区分号错误; [!] 重发帧{}".format(frame_number))
                send_packet(sock2server, seq, frame_number, "正常")

        elif received_data["packet_type"] == PACKET_TYPE["丢包"]:
            paint(frame_number)  # 可视化发送窗口
            print("[*] 什么都没收到")  # 收到丢失消息, 直接假装没收到就行了

        elif received_data["packet_type"] == PACKET_TYPE["误码"]:
            paint(frame_number)  # 可视化发送窗口
            print("[?] 收到误码包; [!] 重发帧{}".format(frame_number))
            send_packet(sock2server, seq, frame_number, "正常")  # 发包误码, 重新发包

        elif received_data["packet_type"] == PACKET_TYPE["否认"]:
            paint(frame_number)  # 可视化发送窗口
            print("[?] 收到 Nak 包; [!] 重发帧{}".format(frame_number))
            send_packet(sock2server, seq, frame_number, "正常")  # 发包不正确, 重新发包
        else:
            raise RuntimeError("[*] 收包不正常")


def add_arguments(arg_parser):
    arg_parser.add_argument("--verbose", "-v", action="store_true", help="是否显示详细信息, 默认不显示")
    arg_parser.add_argument("--probability", "-p", default="70:20:10", type=str,
                            help="设定发包概率, 格式:成功:误码:丢包, 默认值示例:70:20:10")
    arg_parser.add_argument("--timeout", "-t", default=2, type=float,
                            help="设置时延, 发包间隔 TIMEOUT 秒, 超时等待 TIMEOUT * 2.5 秒")
    arg_parser.add_argument("--ip", "-i", default=HOST, type=str,
                            help="设定客户端的 IPv4 地址, 默认值为 {}".format(HOST))
    arg_parser.add_argument("--connect", "-c", default=PORT, type=int,
                            help="设定客户端连接的端口号, 默认值为 {}".format(PORT))


def set_arguments(options):
    global VERBOSE, PROBABILITY, TIMEOUT, HOST, PORT

    VERBOSE = options.verbose
    _1, _2, _3 = [int(x) for x in options.probability.split(":")]
    if _1 + _2 + _3 == 100:
        PROBABILITY["成功"], PROBABILITY["误码"], PROBABILITY["丢包"] = _1, _2, _3
    else:
        print("概率参数设置错误, 将采取默认值-70:20:10")
    TIMEOUT = options.timeout

    if options.ip != "localhost" and options.ip.count(".") != 3:
        print("[*] IP 参数错误, 采取默认值 {}".format(HOST))
    else:
        HOST = options.ip

    if 0 < options.connect < 65536:
        PORT = options.connect
    else:
        print("[*] 端口号错误, 采取默认值 {}".format(PORT))


if __name__ == "__main__":
    # 处理命令行参数
    parser = argparse.ArgumentParser(description="""停等 ARQ 协议-客户端""")
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

        # 循环发帧给服务端的函数
        cycle_send(sock)
    finally:
        sock.close()
