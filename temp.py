#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
import socket
from Crypto.Hash import MD5

__author__ = '__L1n__w@tch'


def test():
    ip = socket.gethostbyname("watch0.top")
    print(ip)


if __name__ == "__main__":
    md5_value = MD5.new(data).hexdigest()
    print(md5_value)