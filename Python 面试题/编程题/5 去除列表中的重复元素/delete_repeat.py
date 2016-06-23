#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 去除列表中重复元素的几种方法
"""

__author__ = '__L1n__w@tch'


def use_set(a_list):
    """
    用集合去除重复元素
    :param a_list: [1,2,1,2]
    :return: [1,2]
    """
    return list(set(a_list))


def use_dictionary(a_list):
    """
    用字典去除重复元素
    :param a_list: [1,2,1,2]
    :return: [1,2]
    """
    a_dict = dict().fromkeys(a_list).keys()
    return list(a_dict)


def use_dict_keep_order(a_list):
    """
    用字典并保持顺序
    :param a_list: [1,2,1,2]
    :return: [1,2]
    """
    another_list = list(set(a_list))
    another_list.sort(key=a_list.index)
    return another_list


def use_list_derive(a_list):
    """
    列表推导式
    :param a_list: [1,2,1,2]
    :return: [1,2]
    """
    another_list = list()
    [another_list.append(i) for i in a_list if i not in another_list]
    return another_list


if __name__ == "__main__":
    List = [1, 2, 1, 2, 3, 3, 3, 4, 1, 0, 9, 9, 3, 1111221231]

    print(use_set(List))
    print(use_dictionary(List))
    print(use_dict_keep_order(List))
    print(use_list_derive(List))

    if use_set(List) == use_dictionary(List) == use_dict_keep_order(List) == use_list_derive(List):
        print("OK")
