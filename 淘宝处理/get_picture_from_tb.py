#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 从淘宝商品页获取主图、详情
"""
import requests
import re

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    # 以下是获取主图
    # url = r"https://detail.tmall.com/item.htm?id=572435654193&sourceType=item&ttid=10001401@taobao_android_8.6.0&ut_sk=1.WjZHrsq287EDAPiQiNo7Sfgw_21646297_1554022685433.GoodsTitleURL.1&un=65e357d3fbea340b9554e02b75a03bae&share_crt_v=1&sp_tk=77%20lSmxvWGJCZEdGQUjvv6U=&cpp=1&shareurl=true&spm=a313p.22.16j.1021930485574&short_name=h.3zDCFw2&sm=583cc0&app=chrome"
    # s = requests.session()
    # response = requests.get(url)
    # with open("test.html","w") as f:
    #     f.write(response.text)
    # with open("test.html") as f:
    #     html = f.read()
    # result = re.findall("""<a href="#"><img src="//(.*)" /></a>""",html)
    # for i,each_main_picture in enumerate(result):
    #     raw_picture = "http://{}".format(each_main_picture[:each_main_picture.rfind("_")])
    #     postfix = raw_picture[raw_picture.rfind("."):]
    #     response = s.get(raw_picture)
    #     with open("./output/主图/{}{}".format(i, postfix), "wb") as f:
    #         f.write(response.content)

    # 以下是获取详情
    url = r"https://desc.alicdn.com/i5/570/430/572435654193/TB16ZLfFVzqK1RjSZFC8qvbxVla.desc%7Cvar%5Edesc%3Bsign%5E7757db41319cb3bd0ec875aba72ab8db%3Blang%5Egbk%3Bt%5E1553846566"
    s = requests.session()
    # response = s.get(url)
    # with open("detail.html","w") as f:
    #     f.write(response.text)
    with open("detail.html") as f:
        html = f.read()
    result = re.findall("""src="[^"]*""",html)
    for i,each_detail in enumerate(result):
        raw_picture = each_detail[len('src="'):]
        postfix = raw_picture[raw_picture.rfind("."):]
        response = s.get(raw_picture)
        with open("./output/详情/{}{}".format(i, postfix), "wb") as f:
            f.write(response.content)