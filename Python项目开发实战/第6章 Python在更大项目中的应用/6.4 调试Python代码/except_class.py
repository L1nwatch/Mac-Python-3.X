#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 创建和使用自定义异常

在Python解释器中运行该脚本,使用-i标签来执行:
python -i except_class.py
当使用-i标签启动Python解释器时,可以传入一个Python文件.而这会导入你传入的文件,而不必显示地在解释器中导入.
'''
__author__ = '__L1n__w@tch'


class TestClass(object):
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def return_values(self):
        try:
            if type(self.number) is int:
                return "The values are: ", type(self.name), type(self.number)
            else:
                raise NotANumber(self.number)
        except NotANumber as e:
            print("The value for number must be an int you passed: ", e.value)


class NotANumber(Exception):
    # 重写了__init__函数,使用value而不是args捕捉了异常中抛出的值
    def __init__(self, value):
        self.value = value

    # 调用repr()方法输出了self.value属性,对于引发异常的值,repr()方法给出该值的正确的表示形式(也就是指打印出来的异常错误消息)
    def __str__(self):
        return repr(self.value)


def main():
    pass


if __name__ == "__main__":
    main()
