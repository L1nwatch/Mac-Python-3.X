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
import threading
import sys

HOST, PORT = "localhost", 23337
# 模拟发包的类型
PACKET_TYPE = {"正常": "Message", "误码": "Error", "丢包": "Lost", "确认": "Ack", "否认": "Nak"}
MAX_FRAME_NUMBER = 15
TIMEOUT = 0.5  # 每隔 1 s 发送一个包


# 网上的超时检测器
class KThread(threading.Thread):
    """A subclass of threading.Thread, with a kill()
    method.
    Come from - Kill a thread in Python:
    http://mail.python.org/pipermail/python-list/2004-May/260937.html
    """

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run  # Force the Thread to install our trace.
        threading.Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the
        trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


# 网上的超时检测器
class Timeout(Exception):
    """function run timeout"""


# 网上的超时检测器
def timeout(seconds):
    """超时装饰器，指定超时时间
    若被装饰的方法在指定的时间内未返回，则抛出Timeout异常"""

    def timeout_decorator(func):
        """真正的装饰器"""

        def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

        def _(*args, **kwargs):
            result = []
            new_kwargs = {  # create new args for _new_func, because we want to get the func return val to result list
                'oldfunc': func,
                'result': result,
                'oldfunc_args': args,
                'oldfunc_kwargs': kwargs
            }
            thd = KThread(target=_new_func, args=(), kwargs=new_kwargs)
            thd.start()
            thd.join(seconds)
            alive = thd.isAlive()
            thd.kill()  # kill the child thread
            if alive:
                raise Timeout(u'function run too long, timeout %d seconds.' % seconds)
            else:
                return result[0]

        _.__name__ = func.__name__
        _.__doc__ = func.__doc__
        return _

    return timeout_decorator


def send_packet(sock, send_seq, frame_number, packet_type):
    """
    负责发包的函数
    :param sock: 套接字
    :param send_seq: 区分号, 0 或 1
    :param frame_number: 帧编号
    :param packet_type: 发包类型
    :return:
    """
    data_dict = dict()
    # 模拟发包情况, 可能正常发包、发包误码、发的包丢失了
    # data_dict["packet_type"] = random.choice(
    #     (PACKET_TYPE["正常"], PACKET_TYPE["误码"], PACKET_TYPE["丢包"])
    # )
    data_dict["packet_type"] = PACKET_TYPE["正常"]
    data_dict["send_seq"] = send_seq
    data_dict["frame_number"] = frame_number

    data = simplejson.dumps(data_dict)
    print("[!] 发送包: {}".format(data))
    sock.sendall(data.encode("utf8"))


# @timeout(TIMEOUT * 2.5)
def receive_packet(sock):
    """
    负责用来收包的函数
    :param sock: 套接字
    :return: dict()
    """
    received_data = sock.recv(1024)
    received_data = simplejson.loads(received_data)
    print("[?] 收到包: {}".format(received_data))

    return received_data


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))

        frame_number, send_seq = 0, 0  # send_seq 作为区分号

        # 发包
        send_packet(sock, send_seq, frame_number, "正常")
        while True:
            try:
                # 期望收到对方发来 Ack 确认
                received_data = receive_packet(sock)
                time.sleep(TIMEOUT * 2.5)
            except Timeout as e:
                # 超时重传在此实现
                print("[*] 超时重传了")
                send_packet(sock, send_seq, frame_number, "正常")
                continue

            # 收到 Ack 确认
            if received_data["packet_type"] == PACKET_TYPE["确认"]:
                # 收到 Ack 应答, 且序号正确, 则发送下一个包
                if received_data["send_seq"] == send_seq:
                    # 产生下一个包的区分号和帧号
                    send_seq = 1 - send_seq
                    # 产生帧编号
                    frame_number = (frame_number + 1) % MAX_FRAME_NUMBER

                    # 发送下一个包
                    send_packet(sock, send_seq, frame_number, "正常")

                # 收到 Ack 应答, 但是序号不对, 重新发包
                else:
                    send_packet(sock, send_seq, frame_number, "正常")
            # 收到丢失消息, 直接假装没收到就行了
            elif received_data["packet_type"] == PACKET_TYPE["丢包"]:
                pass
            # 发包误码, 重新发包
            elif received_data["packet_type"] == PACKET_TYPE["误码"]:
                send_packet(sock, send_seq, frame_number, "正常")
            # 发的包不正确, 重新发包
            elif received_data["packet_type"] == PACKET_TYPE["否认"]:
                send_packet(sock, send_seq, frame_number, "正常")
            else:
                raise RuntimeError("[*] 收包不正常")

    finally:
        sock.close()
