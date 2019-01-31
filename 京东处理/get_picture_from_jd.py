#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 尝试从 jd 导出图片
"""
import requests
import re

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    s = requests.session()
    response = s.get("https://item.jd.com/100000378767.html")
    data = response.text
    all_picture_url = re.findall("<li ><img alt='[^']*' src='[^']*'  data-url='([^']*)' data-img='1' width='50' height='50'></li>",data)
    all_picture_url = re.findall("<li ><img alt='.*", data)
    for i, each in enumerate(all_picture_url):
        picture_true_address = re.findall("data-url='([^']*)'", each)[0]
        picture_true_address_url = "https://img14.360buyimg.com/n1/s546x546_{}".format(picture_true_address)
        postfix = picture_true_address[picture_true_address.rfind("."):]
        response = s.get(picture_true_address_url)
        with open("{}{}".format(i, postfix), "wb") as f:
            f.write(response.content)
