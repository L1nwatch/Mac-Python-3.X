#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 用于把统计数据归一化

由于统计数据的数量级不同, 画在同一张图表的时候差距太多, 所以还是归一化之后再画吧
"""

__author__ = '__L1n__w@tch'


def get_result(a_list):
    # min-max标准化
    # x = (x - min) / (max - min)
    max_value = max(a_list)
    min_value = min(a_list)
    return [(x - min_value) / (max_value - min_value) for x in a_list]


def run():
    search_result = [1212116, 1290553, 2034813, 1922332, 10083]
    search_time = [143109, 1348129, 96360, 76000, 4203]
    index_file = [137, 237, 192, 208, 28.8]
    index_build_time = [85469, 386641, 486985, 666359, 180250]

    print("[*] 检索结果数 依次为: {}".format("\t".join("{0:.2f}".format(x) for x in get_result(search_result))))
    print("[*] 检索耗时 依次为: {}".format("\t".join("{0:.2f}".format(x) for x in get_result(search_time))))
    print("[*] 索引文件空间 依次为: {}".format("\t".join("{0:.2f}".format(x) for x in get_result(index_file))))
    print("[*] 索引建立耗时 依次为: {}".format("\t".join("{0:.2f}".format(x) for x in get_result(index_build_time))))


if __name__ == "__main__":
    run()
