#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 要求是爬去一个网页上的所有专业, 包括统计学校啥的, 时间不够没写好..
"""
import requests

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    tmp_file = "tmp.txt"
    result_file = "result.txt"

    # 模拟回话
    s = requests.Session()

    data = list()
    # 以下是硬编码的
    # 读取网页源码同时把表格数据写入 tmp.txt 中
    with open(tmp_file, "w") as f:
        for page in range(1, 127):
            url = r"http://data.api.gkcx.eol.cn/soudaxue/querySchoolSpecialty.html?messtype=jsonp&zycengci=%E6%9C%AC%E7%A7%91&page={}&size=10&keyWord1=%E8%AE%A1%E7%AE%97%E6%9C%BA&province=&schooltype=&schoolprop=&callback=jQuery183008470115063210626_1468315203918&_=1468315205299".format(
                page)
            response = s.get(url)
            text = response.content.decode("utf8")
            print(text, file=f)

    # 读取临时文件并把合适的结果保存在 result.txt 中
    with open(tmp_file, "r") as f1, open(result_file, "w") as f2:
        for each_line in f1:
            if "schoolname" in each_line or "specialtyname" in each_line:
                print(each_line, end="", file=f2)
