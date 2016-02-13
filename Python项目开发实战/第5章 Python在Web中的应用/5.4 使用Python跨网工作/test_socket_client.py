#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import socket, sys

HOST, PORT = "localhost", 8099


def main():
    data = " ".join(sys.argv[1:])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))
        received = str(sock.recv(1024), "utf-8")
    finally:
        sock.close()

    print("Send:        {}".format(data))
    print("Received:    {}".format(received))


if __name__ == "__main__":
    main()
