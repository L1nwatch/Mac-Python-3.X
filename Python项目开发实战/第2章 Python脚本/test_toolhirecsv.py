#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import csv


def test_reader():
    with open("toolhire.csv") as th:
        toolreader = csv.reader(th)
        print(list(toolreader))


def test_writer():
    items = [
        ['1', 'Lawnmower', 'Small Hover mower', 'Fred', '$150', 'Excellent', '2012-01-05'],
        ['2', 'Lawnmower', 'Ride-on mower', 'Mike', '$370', 'Fair', '2012-04-01'],
        ['3', 'Bike', 'BMX bike', 'Joe', '$200', 'Good', '2013-03-22'],
        ['4', 'Drill', 'Heavy duty hammer', 'Rob', '$100', 'Good', '2013-10-28'],
        ['5', 'Scarifier', 'Quality, stainless steel', 'Anne', '$200', '2013-09-14'],
        ['6', 'Sprinkler', 'Cheap but effective', 'Fred', '$80', '2014-01-06']
    ]
    with open("tooldesc.csv", "w", newline="") as tooldata:
        toolwriter = csv.writer(tooldata)
        for item in items:
            toolwriter.writerow(item)  # writer.writerrow()方法返回写入文件的字符数


def test_dict_form():
    # 即使你的CSV文件不包含标题,也可以使用DictReader. 可以将它读入DictReader然后用DictWriter将它写出来.
    # 这可以弥补这个不足.技巧就是提供标题作为DictReader构造函数的参数
    with open("toolhire.csv") as th:
        rdr = csv.DictReader(th)
        for item in rdr:
            print(item)


def test_analysis():
    # 两种方式对数据进行分析,可以发现第一种的可读性要好一些
    with open("toolhire.csv") as th:
        rdr = csv.DictReader(th)
        items = [item for item in rdr]
    # 第一种
    print([item["Name"] for item in items if item["Owner"] == "Fred"])
    # 第二种
    # [item[1] for item in toolList if item[3] == "Fred"]


def main():
    test_reader()
    test_writer()
    test_dict_form()
    test_analysis()


if __name__ == "__main__":
    main()
