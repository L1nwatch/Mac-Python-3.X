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


if __name__ == "__main__":
    a_int = 3

    print("{sep} 不可变对象 {sep}".format(sep="*" * 30))
    print("调用者: int_id = {}".format(id(a_int)))
    a_int = test_int(a_int)
    print("调用者: int_id = {}".format(id(a_int)))

    a_list = ["aaa"]

    print("{sep} 可变对象 {sep}".format(sep="*" * 30))
    print("调用者: list_id = {}".format(id(a_list)))
    a_list = test_list(a_list)
    print("调用者: list_id = {}".format(id(a_list)))
