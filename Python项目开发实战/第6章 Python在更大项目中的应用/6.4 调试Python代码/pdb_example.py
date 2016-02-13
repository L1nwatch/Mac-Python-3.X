#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Mac OS X 10.10 Python3.4.4下,展示了如何使用pdb模块的能力来调试或检查Python代码

pdb是Python标准库中内置的模块.只需要在文件中导入pdb,然后既可以调用stack_trace()方法进入调试器环境,也可以调用其他方法在运行
时执行文件内的一些特定函数.这会让你进入调试器界面
'''
__author__ = '__L1n__w@tch'

import pdb


class ExampleClass(object):
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def example_entry(self):
        # 运行后应该进入到pdb解释器中
        pdb.set_trace()
        # 输入n(在文件中向下走一行)
        # 输入p self.name并按Enter/Return键后可以打印变量值
        # 输入locals(),看到此时局部作用域内的所有对象(globals()同理,全局作用域内)
        # 在pdb中,c命令只是继续运行程序;如果不想执行余下的程序就退出调试器,在pdb提示符中输入q
        return "The example name is {} with the number {}".format(self.name, self.number)


def main():
    example = ExampleClass("Carla", 456)
    return example.example_entry()


if __name__ == "__main__":
    main()
