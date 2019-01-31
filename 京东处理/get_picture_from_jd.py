#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 尝试从 jd 导出图片
"""
import requests
import re

__author__ = '__L1n__w@tch'


def get_picture(this_session):
    """
    获取主图
    :return:
    """
    response = this_session.get("https://item.jd.com/100000378767.html")
    data = response.text
    all_picture_url = re.findall(
        "<li ><img alt='[^']*' src='[^']*'  data-url='([^']*)' data-img='1' width='50' height='50'></li>", data)
    all_picture_url = re.findall("<li ><img alt='.*", data)
    for i, each in enumerate(all_picture_url):
        picture_true_address = re.findall("data-url='([^']*)'", each)[0]
        picture_true_address_url = "https://img14.360buyimg.com/n1/s546x546_{}".format(picture_true_address)
        postfix = picture_true_address[picture_true_address.rfind("."):]
        response = s.get(picture_true_address_url)
        with open("./主图/{}{}".format(i, postfix), "wb") as f:
            f.write(response.content)


def get_detail(this_session):
    """
    获取详情图
    :param this_session:
    :return:
    """
    url = "https://cd.jd.com/description/channel?skuId=32789142913&mainSkuId=11983165386&cdn=2&callback=showdesc"
    response = this_session.get(url)
    data = response.text
    # with open("test_detail.html", "r") as f:
    #     data = f.read()
    detail_picture = re.findall('data-lazyload=\\\\"//(.*)\\\\"', data)
    for i, each_detail in enumerate(detail_picture):
        response = this_session.get("http://{}".format(each_detail))
        postfix = each_detail[each_detail.rfind("."):]
        with open("./详情/{}{}".format(i, postfix), "wb") as f:
            f.write(response.content)


if __name__ == "__main__":
    s = requests.session()
    get_picture(s)
    get_detail(s)
