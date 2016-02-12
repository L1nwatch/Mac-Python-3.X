#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Mac OS X 10.10 Python3.4.4下测试socketserver模块和http.server模块
'''
__author__ = '__L1n__w@tch'

import socketserver
import http.server

# 注意,变量PORT是全大写的,因为它是常量,在程序中不会改变
PORT = 8099


def main():
    # 请求处理程序
    Handsy = http.server.SimpleHTTPRequestHandler
    # 设置简单的HTTP守护程序或httpd(这是UNIX命名的惯例)
    # http.server模块会在提供的目录(你提供了"",它表示启动服务器时所处的目录)中搜索index.html文件.
    # 如果index.html文件存在,它会提供这个文件.如果文件不存在,http.server会使用list_directory()方法列出当前目录的内容
    httpd = socketserver.TCPServer(("", PORT), Handsy)

    # 需要将目录提供给正确的端口
    httpd.serve_forever()


if __name__ == "__main__":
    main()
