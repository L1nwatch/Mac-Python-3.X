#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.15 想学习一下装饰器的知识, 参考资料:
    http://www.cnblogs.com/rhcad/archive/2011/12/21/2295507.html
"""

__author__ = '__L1n__w@tch'


def wrapper(arg):
    def _for_wrapper(func):
        def _true_wrapper(*args, **kwargs):
            print("[*] 这里的装饰器能够接受参数了: {}".format(arg))
            ret = func(*args, **kwargs)
            print("[*] 最初级的装饰器结束了")
            return ret

        return _true_wrapper

    return _for_wrapper


@wrapper("装饰器4")
def raw_function(a, b):
    print("我有两个参数: {}, {}".format(a, b))
    return a + b


if __name__ == "__main__":
    print("{sep} 原始函数调用开始 {sep}".format(sep="*" * 30))
    result = raw_function(1, 2)
    assert result == 3
    print("{sep} 原始函数调用结束 {sep}".format(sep="*" * 30))
