#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 学习filecmp库, 参考: http://python.jobbole.com/81480/

3 个 test, 分别实现了:
test1(): 比较文件函数filecmp.cmp的相关测试
test2(): 比较文件夹函数filecmp.dircmp的相关测试
test3(): filecmp库自带的dircmp没有递归功能(其实是有的,但是默认却是print()比较结果出来,所以照着源码改了改成能递归比较是否相同)
'''
__author__ = '__L1n__w@tch'

import filecmp
import time
import os


def main():
    # test1()
    # test2()
    test3()


def test3():
    # 测试一下filecmp.dircmp是否能检测出子目录下的不同?
    dir1 = "for_test"
    dir2 = "for_test2"
    dir_cmp = filecmp.dircmp(dir1, dir2)
    print(check_dir_closure(dir_cmp))


# 递归的检查目录, 如果存在不同则返回True, 否则返回None
def check_dir_closure(dir_cmp):
    if len(dir_cmp.left_only) > 0:
        return True
    for sd in dir_cmp.subdirs.values():
        return check_dir_closure(sd)


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
