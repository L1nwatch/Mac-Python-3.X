#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
import requests

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    response = requests.get("http://www.baidu.com")
    print(response.text)
    print(response.content.decode("utf8"))
