#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
__author__ = '__L1n__w@tch'
''' Description
'''

import file_tree


def main():
    help(file_tree)
    print(file_tree.find_files("target.txt", "."))
    print(file_tree.find_files("F.*", "."))
    print(file_tree.find_files(".*\.txt", "."))
    print(file_tree.find_files(".*", "."))


if __name__ == "__main__":
    main()
