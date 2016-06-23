#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 考怎么创建字典的?
"""

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    dictionary = {"key1": 1, "key2": 2}

    items = [("key1", 1), ("key2", 2)]
    dictionary_2 = dict(items)

    dictionary_3 = dict().fromkeys(("key1", "key2"), -1)
    dictionary_4 = dict().fromkeys(("key1", "key2"))

    print(dictionary, dictionary_2, dictionary_3, dictionary_4)
