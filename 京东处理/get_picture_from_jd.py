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
    response = s.get("https://item.jd.com/32789142913.html#none")
    data = response.text
    # https://img14.360buyimg.com/n1/s546x546_jfs/t1/1708/9/2312/90314/5b96253bE4a4680b9/5623409d1acda299.jpg
    # https://img13.360buyimg.com/n5/jfs/t1/1708/9/2312/90314/5b96253bE4a4680b9/5623409d1acda299.jpg
    # jfs/t1/1708/9/2312/90314/5b96253bE4a4680b9/5623409d1acda299.jpg
    # <li ><img alt='美逸 GT20PLUS20000毫安 移动电源 LCD屏显 双向快充QC3.0/2.0 带线 白骑士 白骑士' src='//img13.360buyimg.com/n5/jfs/t1/1708/9/2312/90314/5b96253bE4a4680b9/5623409d1acda299.jpg' data-url='jfs/t1/1708/9/2312/90314/5b96253bE4a4680b9/5623409d1acda299.jpg' data-img='1' width='50' height='50'></li>
    # with open("test.html","w") as f:
    #     f.write(response.text)
    # with open("test.html") as f:
    #     data = f.read()
    all_picture_url = re.findall("<li ><img alt='[^']*' src='[^']*'  data-url='([^']*)' data-img='1' width='50' height='50'></li>",data)
    all_picture_url = re.findall("<li ><img alt='.*", data)
    for i, each in enumerate(all_picture_url):
        picture_true_address = re.findall("data-url='([^']*)'", each)[0]
        picture_true_address_url = "https://img14.360buyimg.com/n1/s546x546_{}".format(picture_true_address)
        postfix = picture_true_address[picture_true_address.rfind("."):]
        response = s.get(picture_true_address_url)
        with open("{}{}".format(i, postfix), "wb") as f:
            f.write(response.content)
