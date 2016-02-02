#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' file_tree.py module containing functions to assist in working with directory hierarchies.
Based on the os.walk() function.
'''
__author__ = '__L1n__w@tch'

import os, re
import os.path as path


def find_files(pattern, base='.'):
    """
    Finds files under base based on pattern
    Walks the file system starting at base and returns a list of filenames matching pattern
    :param pattern:
    :param base:
    :return:
    """
    regex = re.compile(pattern)  # 为了效率而编译了它
    matches = list()
    for root, dirs, files in os.walk(base):
        for f in files:
            if regex.match(f):
                matches.append(path.join(root, f))
    return matches


def test():
    pass


if __name__ == "__main__":
    test()
