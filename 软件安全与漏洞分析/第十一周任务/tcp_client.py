#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 一个正常通信的 TCP 客户端, 对应的 cpp 是 tcp_server.cpp
'''
__author__ = '__L1n__w@tch'

import socket
import sys

HOST, PORT = "192.168.117.131", 9999

if __name__ == "__main__":
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(b"test")

        # Receive data from the server and shut down
        received = sock.recv(1024)

        sock.sendall(b"0")
    finally:
        sock.close()

    print("Sent:     {}".format(b"test"))
    print("Received: {}".format(received))
