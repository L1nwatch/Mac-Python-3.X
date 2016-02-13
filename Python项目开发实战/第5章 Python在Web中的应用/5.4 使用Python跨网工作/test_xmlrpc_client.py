#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 示例客户端

示例想要演示的是可以设置Python来远程执行程序.所以,如果有一个大的数据文件并且想要远程处理它,可以在远程服务器上设置代理,
然后从另一台机器上调用代码
'''
__author__ = '__L1n__w@tch'

# 还有一个http.client库,它允许你通过客户端访问URL.xmlrpc库也通过同样的方式进行设置
import xmlrpc.client

PORT = 8099


def main():
    # 设置一个服务器代理对象
    proxy = xmlrpc.client.ServerProxy("http://localhost:{}".format(PORT))

    # 调用远程过程
    print("the square root of 3 is {}".format(proxy.square(3)))


if __name__ == "__main__":
    main()
