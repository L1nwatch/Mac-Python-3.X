#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 关于类变量和实例变量的讨论
"""

__author__ = '__L1n__w@tch'


class VarTest:
    str_var = "I am 类变量"
    list_var = ["I am 类变量"]


if __name__ == "__main__":
    vt1 = VarTest()
    vt2 = VarTest()

    vt1.str_var = "I am 实例变量"
    print("vt1.str_var: {}".format(vt1.str_var))
    print("vt2.str_var: {}".format(vt2.str_var))
    print("VarTest.str_var: {}".format(VarTest.str_var), end="\n\n")

    # 在实例的作用域里把类变量的引用改变了, 就变成了一个实例变量, self.list_var 不再引用 VarTest 的类变量 list_var 了
    vt1.list_var.append("vt1 到此一游")
    print("vt1.list_var: {}".format(vt1.list_var))
    print("vt2.list_var: {}".format(vt2.list_var))
    print("VarTest.list_var: {}".format(VarTest.list_var))
