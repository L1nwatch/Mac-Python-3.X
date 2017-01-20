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
import sqlite3
import shelve

__author__ = '__L1n__w@tch'


def count_gz_to_pcap():
    """
    统计一下从 gz 到 pcap 包的数量
    :return: pcap 包总数
    """
    pcap_counts = 0

    for root, dirs, files in os.walk("full_test"):
        for each_file in files:
            if each_file.endswith(".pcap"):
                pcap_counts += 1

    print("[*] 总共测试 {} 个 pcap 包".format(pcap_counts))

    with shelve.open("2th_headers_result.dat") as f:
        data_dict = f["data"]

    http_counts = 0
    for each_pcap_http_request in data_dict:
        http_counts += len(data_dict[each_pcap_http_request])

    print("[*] 总共提取出 {} 个 pcap 包中的 HTTP 请求, HTTP 请求一共 {} 个".format(len(data_dict), http_counts))

    return pcap_counts


def count_http_to_useful_rule():
    """
    统计一下有效样本数
    """
    with open("efficient_pcap.json", "r") as f:
        data = json.load(f)

    efficient_sid_counts = 0
    for each_pcap_http_request in data:
        efficient_sid_counts += len(data[each_pcap_http_request])

    print("[*] 总共获得 {} 个有效样本, HTTP 请求一共 {} 个".format(len(data), efficient_sid_counts))


def count_sample_httpobj_number():
    """
    读取数据库, 看最终写入数据库的有多少条
    """
    waf_ips_number = 0
    utm_number = 0

    with sqlite3.connect("test.lib") as cursor:
        result = cursor.execute("SELECT count(*) FROM sample_utm;")
        utm_number = result.fetchone()[0]
        print("[*] 数据库 sample_utm 一共有样本 {} 条".format(utm_number))

        result = cursor.execute("SELECT count(*) FROM  sample_waf_ips;")
        waf_ips_number = result.fetchone()[0]
        print("[*] 数据库 sample_waf_ips 一共有样本 {} 条".format(waf_ips_number))

    return waf_ips_number, utm_number


def count_utm_urls_number():
    """
    读取 utm url json 文件, 看有多少条数据
    :return:
    """
    with open("utm_url_result.json", "r") as f:
        data = json.load(f)

    url_number = len(data)

    print("[*] 获取 {} 条 URL 样本".format(url_number))

    return url_number


if __name__ == "__main__":
    total_pcap_number = count_gz_to_pcap()
    count_http_to_useful_rule()
    efficient_utm_urls = count_utm_urls_number()
    waf_ips_number, utm_number = count_sample_httpobj_number()
    print("UTM: {}".format(utm_number / efficient_utm_urls))
    print("WAF/IPS: {}".format(waf_ips_number / total_pcap_number))
