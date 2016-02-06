#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' shelve模块示例
'''
__author__ = '__L1n__w@tch'

import shelve


class Test:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        print(self.x, self.y)


def test1():
    shelf = shelve.open("fundata.shelve", "c")  # 首先创建了一个shelve数据库文件(或者,它们有时被称为shelf)
    # 向shelf中添加记录, 不需要任何数据转换:
    shelf["tuple"] = (1, 2, "a", "b", True, False)
    shelf["lists"] = [[1, 2, 3], [True, False], [3.14159, -66]]

    # 可以通过读回值来检查shelve已经保存的项
    print(shelf["tuple"])
    print(shelf["lists"])

    # 为了永久保存数据的变化,需要调用close(通常,会使用一个try/finally结构体,或不同于dbm,可以使用上下文管理器样式)
    # 在关闭shelf之后,不能再访问数据了
    shelf.close()


def test2():
    with shelve.open("test.shelve", "c") as shelf:
        a = Test(1, 2)
        a.show()
        b = Test("a", "b")
        b.show()
        shelf["12"] = a
        shelf["ab"] = b

        # 注意,返回的对象被称为__main__.Test对象.这会引发一个关于保存和恢复用户自定义类的非常重要的警告
        # 你必须确保shelf用于保存的类定义也同样适用于从shelf读回类的模块,并且类定义必须一致
        # 如果在写数据和读数据期间类定义发生了改变,结果将会变得不可预知.让类可见的常见做法是把它放入自己的模块
        # 之后这个模块可以被导入,并在写入和读取shelf的代码中使用
        c = shelf["12"]
        c.show()
        d = shelf["ab"]
        d.show()


def main():
    test1()
    test2()


if __name__ == "__main__":
    main()
