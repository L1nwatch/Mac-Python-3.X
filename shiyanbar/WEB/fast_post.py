#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' http://www.shiyanbar.com/ctf/1854
先查看响应头,发现了 Base64 编码的 FLag
解码后得到: P0ST_THIS_T0_CH4NGE_FL4G:LsnrrTIdu
再根据源码中的提示,用 POST 方式进行快速提交

后来才发现,每次访问网页的 FLAG 都是不同的,所以得用程序获取 flag 后在进行提交

可以得到的东西有: "FLAG", Base64, 解码后aaa:bbb 共四种东西
组合方式:
FLAG=base64 ×
FLAG=aaa    ×
FLAG=bbb    ×
FLAG=aaa:bbb(bbb:aaa)   ×
FLAG=base64:aaa         ×
FLAG=base64:bbb         ×
FLAG=base64:aaa:bbb     ×
base64=aaa:bbb(bbb:aaa) ×
base64=bbb              ×
base64=aaa              ×
aaa=bbb     ×
bbb=aaa     ×
FLAG=base64,aaa:bbb     ×
FLAG:aaa=bbb            ×

..看了 Writeup 后才知道,post 参数名字应该命名为 key,参考注释:
<!-- please post what you find with parameter:key -->
'''
__author__ = '__L1n__w@tch'

import requests
import base64


def main():
    url = "http://ctf4.shiyanbar.com/web/10.php"
    s = requests.Session()
    response = s.get(url)

    parameter = response.headers["FLAg"]
    key, value = base64.b64decode(parameter).decode("utf8").split(":")
    post_data = {"key": value}
    print("Post data: {}".format(post_data), end="\n\n")
    response = s.post(url, data=post_data)

    # print Result
    print(response.text)


if __name__ == "__main__":
    main()
