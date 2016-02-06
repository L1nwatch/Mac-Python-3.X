#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 练习pickle模块的dump()函数和load()函数
'''
__author__ = '__L1n__w@tch'

import pickle


def main():
    an_item = ["1", "Lawnmower", "Tool", "1", "$150", "Excellent", "2012 - 01 - 05"]
    with open("item.pickle", "wb") as pf:
        pickle.dump(an_item, pf)

    with open("item.pickle", "rb") as pf:
        item_copy = pickle.load(pf)

    print(item_copy)

    fun_data = ("a string", True, 42, 3.14159, ["embeded", "list"])
    with open("data.pickle", "wb") as pf:
        pickle.dump(fun_data, pf)

    with open("data.pickle", "rb") as pf:
        copy_data = pickle.load(pf)
        print(copy_data)


if __name__ == "__main__":
    main()
