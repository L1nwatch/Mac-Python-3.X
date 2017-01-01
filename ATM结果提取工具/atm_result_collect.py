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


def recursion_get_rate(json_data, depth_layer=None, format_display_style=1):
    """
    递归解析 json 树, 获取对应模块及其成功率
    :param json_data: 解析好的 json 数据
    :param depth_layer: 限制最深读取到第几层
    :param format_display_style: 可以分为几种不同的格式进行打印
    :return: list(), 每个元素是其模块及其成功率
    """

    def __recursion_get_rate(json_list, a_list, layer, depth_limit=None, style=1):
        temp_list = list()

        # 到了限定的最后一层了
        if depth_limit:  # 为 0 时显示全部
            if layer >= depth_limit:
                return temp_list
        # 递归处理
        for each in json_list:
            if style == 1:
                temp_list.append("{sep}{0} => {1}".format(each["name"], each["percent"], sep=" " * layer))
            elif style == 2:
                temp_list.append("{sep}{0}【{1}】".format(each["name"], each["percent"], sep=" " * layer))
            elif style == 3:
                temp_list.append("{0}成功率【{1}】".format(each["name"], each["percent"]))
            elif style == 4:
                format_text = "{sep}{0} => {1}".format(each["name"], each["percent"], sep="{}  +- ".format("  |" * layer))
                temp_list.append(format_text)

            if len(each["children"]) > 0:
                __recursion_get_rate(each["children"], temp_list, layer + 1, depth_limit, style)

        return a_list.extend(temp_list)

    result_list = list()

    __recursion_get_rate(json_data, result_list, 0, depth_layer, format_display_style)

    return result_list


def get_json_data_from_result_url(url):
    response = requests.get("{}/rsuites".format(url))
    parse_data = json.loads(response.text)
    return parse_data


if __name__ == "__main__":
    result_url = "http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec/results/585f344dd10540715b07f011"
    json_result = get_json_data_from_result_url(result_url)
    result = recursion_get_rate(json_result, 4)

    for each_module in result:
        print(each_module)
