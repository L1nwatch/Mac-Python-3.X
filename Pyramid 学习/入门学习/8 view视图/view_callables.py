#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" view callable 相关知识
"""
from pyramid.response import Response
from pyramid.httpexceptions import HTTPUnauthorized

__author__ = '__L1n__w@tch'


# view callable 就是 view 的全称，它可以是一个函数
def hello_world(request):
    return Response("Hello World!")


# 也可以是一个类
class MyView(object):
    # 注意这种写法, 我们将 request 对象作为参数传递给类的构造函数, 并赋值给 self, 这样在类的其他方法中就只需要传递 self 参数了
    def __init__(self, request):
        self.request = request

    def __call__(self, *args, **kwargs):
        return Response("Hello World!")


# view callable response
# 通常情况下, 我们应该返回 pyramid.response.Response 的一个实例
# 但是如果抛出异常, 可能需要返回一个 http exception 对象
def a_view(request):
    # 这段代码将返回 http 401 错误
    raise HTTPUnauthorized()

# 你也可以像下面这样，用 pyramid.httpexceptions.exception_response() 直接返回 http 状态码


if __name__ == "__main__":
    pass
