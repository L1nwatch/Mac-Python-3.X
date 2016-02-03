#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 以下为tooldesc2.csv文件定义了一组标题,然后打开文件把它读入到一个DictReader对象.然后使用DictWriter将数据写到新文件.
它会自动地插入一个标题行.
'''
__author__ = '__L1n__w@tch'

import csv


def main():
    fields = ["ItemID", "Name", "Description", "Owner", "Price", "Condition", "DateRegistered"]
    with open("tooldesc2.csv") as td_in:
        rdr = csv.DictReader(td_in, fieldnames=fields)
        items = [item for item in rdr]
    with open("tooldesc3.csv", "w", newline="") as td_out:
        wrt = csv.DictWriter(td_out, fieldnames=fields)
        wrt.writeheader()
        wrt.writerows(items)


if __name__ == "__main__":
    main()
