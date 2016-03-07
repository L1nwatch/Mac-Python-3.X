#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://ctf4.shiyanbar.com/ppc/acsii.php
'''
__author__ = '__L1n__w@tch'

import requests
import re

num_dict = {
    r"&nbsp;xxx&nbsp;<br />x&nbsp;&nbsp;&nbsp;x&nbsp;<br />&nbsp;&nbsp;xx&nbsp;<br />&nbsp;x&nbsp;&nbsp;&nbsp;<br />xxxxx<br />": 2,
    r"&nbsp;xx<br>&nbsp;&nbsp;x&nbsp;x&nbsp;&nbsp;<br>&nbsp;&nbsp;x&nbsp;&nbsp;<br>&nbsp;&nbsp;x&nbsp;&nbsp;<br>xxxxx<br>": 1,
    r"&nbsp;xxx&nbsp;<br />x&nbsp;&nbsp;&nbsp;x<br />x&nbsp;&nbsp;&nbsp;x<br />x&nbsp;&nbsp;&nbsp;x<br />&nbsp;xxx&nbsp;<br />": 0,
    r"&nbsp;xxx&nbsp;<br />x&nbsp;&nbsp;&nbsp;x<br />&nbsp;&nbsp;xx&nbsp;<br />x&nbsp;&nbsp;&nbsp;x<br />&nbsp;xxx&nbsp;<br />": 8,
    r"&nbsp;x&nbsp;&nbsp;&nbsp;x<br />x&nbsp;&nbsp;&nbsp;&nbsp;x<br />&nbsp;xxxxx<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;x<br />&nbsp;&nbsp;&nbsp;&nbsp;x<br />": 4,
    r"xxxxx<br />x&nbsp;&nbsp;&nbsp;&nbsp;<br />&nbsp;xxxx<br />&nbsp;&nbsp;&nbsp;&nbsp;x<br />xxxxx<br />": 5
}


def get_div_tag(text):
    """
    获取网页源码中 div 部分的内容
    :param text: <html>...</html>
    :return: <div ..>(...)</div> PS: 仅返回括号里的内容
    """
    res = re.findall(r"<div.*", text)[1]  # 得到 <div name=....>....</div>
    res = re.match(r"<div[^>]*>(.*)</div>", res).groups()[0]
    return res


def get_num(string):
    """
    从 div 源码中得到数字
    :param string: "&nbsp;xx<br>&nbsp;.....<br/><br/><br/>"
    :return: 12345
    """
    position = list()
    # 查找每个数字出现的位置, 得到的结果类似于
    # [(1, 0), (2, 799), (2, 1219), (0, 130), (0, 370), (0, 505), (0, 935), (5, 255), (4, 640), (4, 1065)]
    for key, value in num_dict.items():
        pos = string.find(key)
        while pos > -1:
            position.append((value, pos))
            pos = string.find(key, pos + 1)

    # 对位置进行排序
    # [(1, 0), (0, 130), (5, 255), (0, 370), (0, 505), (4, 640), (2, 799), (0, 935), (4, 1065), (2, 1219)]
    position = sorted(position, key=lambda x: x[1])

    # 把数字拼接出来: 1050042042
    return "".join([str(x[0]) for x in position])


def main():
    url = "http://ctf4.shiyanbar.com/ppc/acsii.php"
    s = requests.Session()

    response = s.get(url)
    num_str = get_div_tag(response.text)
    num = get_num(num_str)
    response = s.post(url, data={"inputNumber": num})
    print(response.text)


if __name__ == "__main__":
    main()
