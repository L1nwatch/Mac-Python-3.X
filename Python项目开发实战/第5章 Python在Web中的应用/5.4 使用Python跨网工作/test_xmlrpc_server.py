#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 示例搭建了一个XML-RPC服务器.它会在本地的一个终端上运行并且提供一个简单的Python脚本.
然后打开另一个Terminal窗口并远程运行代码
'''
__author__ = '__L1n__w@tch'

from xmlrpc.server import SimpleXMLRPCServer

PORT = 8099


def square(n):
    return n * n


def main():
    server = SimpleXMLRPCServer(("localhost", PORT))
    print("We've got a connection and are listening on port {}...huzzah".format(PORT))

    # 注册函数,这样它可以被即将创建的客户端代码使用
    server.register_function(square, "square")

    # 启动服务器
    server.serve_forever()


if __name__ == "__main__":
    main()
