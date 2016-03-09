#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://www.shiyanbar.com/ctf/1841
给你一个sha1值，它是0-100000之间的整数的md5值再求取sha1值，请在2秒内提交该整数值
'''
__author__ = '__L1n__w@tch'

import requests
import re
from Crypto.Hash import SHA
from Crypto.Hash import MD5


def get_div_tag(text):
    """
    获取网页源码中 div 部分的内容
    :param text: <html>...</html>
    :return: <div ..>(...)</div> PS: 仅返回括号里的内容
    """
    res = re.findall(r"<div.*</div>", text)[0]  # 得到 <div name=....>....</div>
    res = re.match(r"<div[^>]*>(.*)</div>", res).groups()[0]
    return res


def brute_force(hash):
    for num in range(100000):
        md5 = MD5.new(bytes(str(num), "utf8")).hexdigest().encode("utf8")
        sha1 = SHA.new(md5).hexdigest()
        if sha1 == hash:
            return num


def main():
    url = "http://ctf4.shiyanbar.com/ppc/sd.php"
    s = requests.Session()
    response = s.get(url)
    md5_sha1 = get_div_tag(response.text)
    num = brute_force(md5_sha1)
    post_data = {"inputNumber": num}
    response = s.post(url, post_data)
    print(response.text)


if __name__ == "__main__":
    main()
