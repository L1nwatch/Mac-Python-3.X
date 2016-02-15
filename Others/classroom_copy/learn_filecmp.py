#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 测试filecmp库, 参考: http://python.jobbole.com/81480/
'''
__author__ = '__L1n__w@tch'

import filecmp
import time
import os


def main():
    # test1()
    test2()


def test2():
    test_dir1 = r"for_test"
    test_file1 = os.path.join(test_dir1, "test1")
    test_dir2 = r"for_test2"
    test_file2 = os.path.join(test_dir2, "test1")

    with open(test_file1, "w") as f:
        f.write("1")

    with open(test_file2, "w") as f:
        f.write("1")

    print(filecmp.dircmp(test_dir1, test_dir2).left_only)

    time.sleep(1)

    with open(test_file2, "w") as f:
        f.write("2")
    print(filecmp.dircmp(test_dir1, test_dir2).diff_files)


def test1():
    test_file1 = "test1"
    test_file2 = "test2"

    with open(test_file1, "w") as f:
        f.write("1")

    with open(test_file2, "w") as f:
        f.write("3")

    # 如果指定最后一个参数为True, 容易导致匹配失败, 原因是两个文件创建时间太近了, 其余参数又太相像
    print(filecmp.cmp(test_file1, test_file2, False))


if __name__ == "__main__":
    main()
