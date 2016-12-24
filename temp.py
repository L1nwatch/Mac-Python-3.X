#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
__author__ = '__L1n__w@tch'


def test_int(a_int):
    print("被调用者: a_int_id = {}".format(id(a_int)))
    a_int += 1
    return a_int


def test_list(a_list):
    print("被调用者: a_list_id = {}".format(id(a_list)))
    a_list.append("bbb")
    return a_list


def temp(old_list):
    new_list = old_list[:]
    number = new_list.count("")
    for i in range(number):
        old_list.remove("")

    return old_list


if __name__ == "__main__":
    usr = 0

    with open("allcpu22.txt", "r") as f:
        counts = 0
        for each_line in f:
            counts += 1
            if counts < 4:
                # 跳过前 3 行
                continue
            each_line = each_line.split(" ")
            each_line = temp(each_line)
            usr += float(each_line[3])

    print(usr)
