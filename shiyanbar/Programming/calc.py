#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://www.shiyanbar.com/ctf/31
题目,计算网页中的 (8853 + 413) x (7756 - 29) - (835 + 972 - 421) x 918 就行了
'''
__author__ = '__L1n__w@tch'

import requests
import re


def get_expression(text):
    text = get_div_tag(text)
    text = text.replace("x", "*")
    return text


def get_div_tag(text):
    """
    获取网页源码中 div 部分的内容
    :param text: <html>...</html>
    :return: <div ..>(...)</div> PS: 仅返回括号里的内容
    """
    expression_div = 3
    res = re.findall(r"<div.*</div>", text)[expression_div]  # 得到 <div name=....>....</div>
    res = re.match(r"<div[^>]*>(.*)</div>", res).groups()[0]
    return res


def main():
    url = "http://ctf8.shiyanbar.com/jia/"
    s = requests.Session()
    response = s.get(url)
    expression = get_expression(response.text)

    # 学习一下 eval, 居然可以直接进行计算
    value = eval(expression)
    post_data = {"pass_key": value}

    print("Expression: {}, Post_data: {}".format(expression, post_data), end="\n\n")

    response = s.post(url + "?action=check_pass", post_data)
    print(response.content.decode("gb2312"))


if __name__ == "__main__":
    main()
