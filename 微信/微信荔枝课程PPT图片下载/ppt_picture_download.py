#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
import requests

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    for i in range(30):
        url = "https://img.lycheer.net/ppt/31665998/1581675083089-0000{}.png/ppt1280q70".format(str(i).zfill(2))
        with open("{}.png".format(i), "wb") as f:
            response = requests.get(url)
            f.write(response.content)
