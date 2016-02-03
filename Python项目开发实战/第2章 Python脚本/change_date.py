#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 从tooldesc.csv文件读取工具列表,然后从列表中提取每个时期域,转换成日期格式,最后将这个数据写回到CSV文件中
'''
__author__ = '__L1n__w@tch'

import csv
from datetime import datetime


def convert_date(item):
    the_date = item[-1]
    date_obj = datetime.strptime(the_date, "%Y-%m-%d")  # 四位数字年%Y,两位数字月份%m,两位数字天%d
    date_str = datetime.strftime(date_obj, "%m/%d/%Y")
    item[-1] = date_str
    return item


def main():
    with open("tooldesc.csv") as td:
        rdr = csv.reader(td)
        items = list(rdr)

    for i in items:
        print(i)

    items = [convert_date(item) for item in items]
    with open("tooldesc2.csv", "w", newline="") as td:
        wrt = csv.writer(td)
        for item in items:
            wrt.writerow(item)


if __name__ == "__main__":
    main()
