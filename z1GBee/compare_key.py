#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 对两串密钥进行比较
'''
__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    key_1 = "1 0 0 1 0 0 0 1 1 0 1 0 1 0 1 1"
    key_2 = "0 0 0 1 1 1 0 0 1 1 1 1 0 1 1 1"

    counts = 0
    print("Key1:\n{}\nKey2:\n{}".format(key_1, key_2))
    for i in range(len(key_1)):
        if key_1[i] == " ":
            print("", end=" ")
            continue
        elif key_1[i] == key_2[i]:
            print(".", end="")
        else:
            counts += 1
            print("!", end="")

    print("")
    print("Different bit: {}".format(counts))
