#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 使用ElementTree XML解析器提取之前示例中一样的日期.同时也为电子表格中的物品计算平均接触时间.
'''
__author__ = '__L1n__w@tch'

import xml.etree.ElementTree as ET
import datetime as dt  # 为了之后的日期计算


def parse_dates(file_name):
    """
    该函数首先将XML文件解析到一个DOM钟,注意接受的参数是文件名而不是文件对象
    :param file_name:
    :return:
    """
    dates = list()
    rows = list()
    dom = ET.parse(file_name)
    root = dom.getroot()  # 使用getroot()方法从DOM中获得根节点
    for node in dom.iter("*"):  # 使用iter()方法来查找所有的文件, 这是通过*参数指定的
        if "Row" in node.tag:  # 检查节点的标签中是否存在Row
            rows.append(node)

    for row in rows:  # 深入到每一行中检查每个节点,寻找key为Type和value为Datetime的节点
        row_dates = list()
        for node in row.iter("*"):
            for key, value in node.attrib.items():
                if "Type" in key and "DateTime" in value:
                    row_dates.append(node.text)
            if len(row_dates) == 2:
                dates += row_dates
    return dates


def calculate_average(dates):
    loan_periods = list()
    while dates:
        # 需要分割字符串,因为datetime.strptime()方法不能处理小数的秒值
        lent = dates.pop(0).split("T")[0]
        ret = dates.pop(0).split("T")[0]
        lent_date = dt.datetime.strptime(lent, "%Y-%m-%d")
        ret_date = dt.datetime.strptime(ret, "%Y-%m-%d")
        loan_periods.append((ret_date - lent_date).days)  # datetime对象
    average = sum(loan_periods) / len(loan_periods)
    return average


def main():
    dates = parse_dates("toolhire.xml")
    avg = calculate_average(dates)
    print("Average loan period is: {} days".format(avg))


if __name__ == "__main__":
    main()
