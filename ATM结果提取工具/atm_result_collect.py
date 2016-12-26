#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.26 ATM 结果提取工具
"""
import requests

try:
    import simplejson as json
except ImportError:
    import json

__author__ = '__L1n__w@tch'


def recursion_get_rate(json_data, depth_layer=None):
    """
    递归解析 json 树, 获取对应模块及其成功率
    :param json_data: 解析好的 json 数据
    :param depth_layer: 限制最深读取到第几层
    :return: list(), 每个元素是其模块及其成功率
    """

    def __recursion_get_rate(json_list, a_list, layer, depth_limit=None):
        temp_list = list()

        # 到了限定的最后一层了
        if depth_limit:
            if layer >= depth_limit:
                return temp_list
        # 递归处理
        for each in json_list:
            temp_list.append("{sep}{0} => {1}".format(each["name"], each["percent"], sep=" " * layer))
            if len(each["children"]) > 0:
                __recursion_get_rate(each["children"], temp_list, layer + 1, depth_limit)

        return a_list.extend(temp_list)

    result_list = list()

    __recursion_get_rate(json_data, result_list, 0, depth_layer)

    return result_list


if __name__ == "__main__":
    result_url = "http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec/results/585f344dd10540715b07f011"
    response = requests.get("{}/rsuites".format(result_url))
    parse_data = json.loads(response.text)
    result = recursion_get_rate(parse_data, 4)

    for each_module in result:
        print(each_module)
