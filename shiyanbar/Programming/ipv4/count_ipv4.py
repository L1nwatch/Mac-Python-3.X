#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://www.shiyanbar.com/ctf/723
参考了 WP 之后才知道每一行还有 IP 地址分配的数量, 得把这个加上去
'''
__author__ = '__L1n__w@tch'


def main():
    file_name = "delegated-apnic-20140223.txt"
    counts = 0
    with open(file_name) as f:
        data = f.readlines()
    for each in data:
        if each.startswith("apnic") and "CN" in each and "ipv4" in each:
            num = each.split("|")[4]
            counts += int(num)
    print("Counts: {}".format(counts))


if __name__ == "__main__":
    main()
