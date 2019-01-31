#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 尝试从 jd 导出图片
"""
import os

import requests
import shutil
import re

__author__ = '__L1n__w@tch'


def get_picture(this_session, request_url):
    """
    获取主图
    :return:
    """
    response = this_session.get(request_url)
    data = response.text

    # 获取 id 信息,方便下载详情图
    sku_id, main_sku_id = re.findall('qualityLife: "//c.3.cn/qualification/info\?skuId=(\d*)&pid=(\d*)', data)[0]

    # 下载主图
    all_picture_url = re.findall("<li ><img alt='.*", data)
    for i, each in enumerate(all_picture_url):
        picture_true_address = re.findall("data-url='([^']*)'", each)[0]
        picture_true_address_url = "https://img14.360buyimg.com/n1/s546x546_{}".format(picture_true_address)
        postfix = picture_true_address[picture_true_address.rfind("."):]
        response = s.get(picture_true_address_url)
        with open("./主图/{}{}".format(i, postfix), "wb") as f:
            f.write(response.content)
    return sku_id, main_sku_id


def get_detail(this_session, sku_id, main_sku_id):
    """
    获取详情图
    :param this_session:
    :return:
    """
    raw_url = "https://cd.jd.com/description/channel?skuId={}&mainSkuId={}&cdn=2&callback=showdesc"
    url = raw_url.format(sku_id, main_sku_id)
    response = this_session.get(url)
    data = response.text
    detail_picture = re.findall('data-lazyload=\\\\"//(.*?)\\\\"', data)
    for i, each_detail in enumerate(detail_picture):
        response = this_session.get("http://{}".format(each_detail))
        postfix = each_detail[each_detail.rfind("."):]
        with open("./详情/{}{}".format(i, postfix), "wb") as f:
            f.write(response.content)


def clear_old():
    """
    清除之前下载过的文件
    :return:
    """
    shutil.rmtree("./主图")
    shutil.rmtree("./详情")
    os.makedirs("./主图", exist_ok=True)
    os.makedirs("./详情", exist_ok=True)


if __name__ == "__main__":
    request_url = "https://item.jd.com/3889259.html"

    clear_old()
    s = requests.session()
    sku_id, main_sku_id = get_picture(s, request_url)
    get_detail(s, sku_id, main_sku_id)
