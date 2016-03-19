#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://www.shiyanbar.com/ctf/1850
用 Linux 命令 file 判断完文件类型后, 知道是 Linux rev 1.0 ext2 filesystem data
WP 说可以用 mount 挂载,或者 binwalk -e sos 直接提取得到 200 多个小文件
这个程序的目的就是把这 200 多个小文件的内容合在一起打印出来
'''
__author__ = '__L1n__w@tch'


def main():
    contents = b""
    for i in range(242):
        with open("_sos.extracted/" + str(i + 1), "rb") as f:
            contents += f.read()
    print(contents, end="")


if __name__ == "__main__":
    main()
