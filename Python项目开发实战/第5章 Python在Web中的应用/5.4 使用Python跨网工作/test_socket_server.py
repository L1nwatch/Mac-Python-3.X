#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 将再次设置一个服务器和一个客户端,然而,会创建一个类来处理TCP请求
'''
__author__ = '__L1n__w@tch'

import socketserver

HOST, PORT = "localhost", 8099


# 为请求处理程序创建类.这个类会在每次连接中被实例化一次
class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper - cased
        self.request.sendall(self.data.upper())


def main():
    server = socketserver.TCPServer((HOST, PORT), TCPHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
