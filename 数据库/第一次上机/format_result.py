#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 鉴于 Numbers 以及 Pages 都没有将表格多行分栏显示的功能, 自己手动用 Python 进行分栏操作然后手动复制粘贴进去表格好了
于是需要用 Python 来均分, 分隔符是 Tab 符号
'''
__author__ = '__L1n__w@tch'

from collections import OrderedDict
import os
import math


def divide_rows(data):
    """
    将 data 分组
    :param data: <class 'list'>: ['student_number\tstudent_score\n', '03051001\t63\n', ... ]
    :return: OrderedDict(), such as {"1":list(), "2":list(), "3":[1\t11, 2\t22, 3\t33]}
    """
    datas = OrderedDict()

    for column in range(columns):
        if column == columns - 1 and (column + 1) * rows >= len(data):
            data_per_row_column = data[column * rows:]
        else:
            data_per_row_column = data[column * rows: (column + 1) * rows]
        datas[column] = data_per_row_column

    return datas


def divide_rows_to_file(file_name, data):
    with open(path + os.sep + "result_" + file_name, "w") as f:
        for i in range(columns):
            print("{}".format(data[0].strip()), file=f, end="\t")
        print("", file=f)

        datas = divide_rows(data[1:])

        # 打印每一行
        for row in range(rows):
            # 打印每一栏
            for column in range(columns):
                if row < len(datas[column]):
                    print("{}".format(datas[column][row].strip()), file=f, end="\t")
                else:
                    break
            print("", file=f)


if __name__ == "__main__":
    global path, columns, rows
    path = "result"
    columns = 3  # 分成三栏

    for i in range(1, 16 + 1):
        file_path = path + os.sep + str(i) + ".txt"
        with open(file_path, "r") as f:
            data = f.readlines()
            rows = math.ceil((len(data) - 1) / columns)  # 每栏多少行
            divide_rows_to_file(str(i) + ".txt", data)
