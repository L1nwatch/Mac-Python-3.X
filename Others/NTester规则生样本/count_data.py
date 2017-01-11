#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.10 写报告用的, 用来统计自己的转换情况的
"""
try:
    import simplejson as json
except ImportError:
    import json

import os

__author__ = '__L1n__w@tch'


def count_gz_to_pcap():
    """
    统计一下从 gz 到 pcap 包的数量
    """
    pcap_counts = 0

    for root, dirs, files in os.walk("full_test"):
        for each_file in files:
            if each_file.endswith(".pcap"):
                pcap_counts += 1

    print("总共测试 {} 个 pcap 包".format(pcap_counts))

    with open("2th_headers_result.json", "r") as f:
        data = json.load(f)

    http_counts = 0
    for each_pcap_http_request in data:
        http_counts += len(data[each_pcap_http_request])

    print("总共提取出 {} 个 pcap 包中的 HTTP 请求, HTTP 请求一共 {} 个".format(len(data), http_counts))


def count_http_to_useful_rule():
    """
    统计一下有效样本数
    """
    with open("efficient_pcap.json", "r") as f:
        data = json.load(f)

    efficient_sid_counts = 0
    for each_pcap_http_request in data:
        efficient_sid_counts += len(data[each_pcap_http_request])

    print("总共获得 {} 个有效样本, HTTP 请求一共 {} 个".format(len(data), efficient_sid_counts))


if __name__ == "__main__":
    count_gz_to_pcap()
    count_http_to_useful_rule()
    print(2947 / 8167)
