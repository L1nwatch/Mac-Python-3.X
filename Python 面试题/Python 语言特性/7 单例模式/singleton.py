#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 单例模式的 4 种实现方法

1. 使用__new__方法
2. 共享属性(创建实例时把所有实例的 __dict__ 指向同一个字典,这样它们具有相同的属性和方法)
3. 装饰器版本
4. import方法
"""
from singleton_for_import import my_singleton

__author__ = '__L1n__w@tch'


# 使用 __new__ 方法
class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance


class TestSingleton1(Singleton):
    var = 1


"""
共享属性的方法, 不知道为何出错了
class Singleton2:
    _state = {}

    def __new__(cls, *args, **kwargs):
        ob = super(Singleton2, cls).__new__(cls, *args, **kwargs)
        ob.__dict__ = cls._state
        return ob


class TestSingleton2(Singleton2):
    var = 2
"""


def singleton(cls, *args, **kwargs):
    instances = dict()

    def get_instance():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class TestSingleton3:
    var = 3


if __name__ == "__main__":
    ts1 = TestSingleton1()
    ts2 = TestSingleton1()
    assert ts1 == ts2  # 仅有一个实例

    # ts3 = TestSingleton2()
    # ts4 = TestSingleton2()
    # assert ts3 == ts4

    ts5 = TestSingleton3()
    ts6 = TestSingleton3()
    assert ts5 == ts6

    my_singleton.foo()  # import 到的本身就是一个实例
