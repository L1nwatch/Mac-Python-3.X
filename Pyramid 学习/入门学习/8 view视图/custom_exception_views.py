#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 你可以自定义异常视图
"""
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

__author__ = '__L1n__w@tch'


# Custom Exception Views
# 你可以自定义异常视图. 为了自定义异常视图, 你需要创建一个 Exception 类或者 Exception 的子类
# 并设置它为你想调用的那个视图的 view configuration 的 context 上下文
class ValidationFailure(Exception):
    def __init__(self, msg):
        self.msg = msg


# 然后配置以下视图, 当你在其他地方抛出 helloWorld.exceptions.ValidationFailure 异常时就会调用这段自定义的视图了
@view_config(context=ValidationFailure)
def failed_validation(exc, request):
    response = Response("Failed validation: {}".format(exc.msg))
    response.status_int = 500
    return response


# 你还可以为特定的路由配置 Exception, 比如下面这段专门为 home 路由配了一个 ValidationFailure
@view_config(context=ValidationFailure, route_name="home")
def failed_validation2(exc, request):
    response = Response("Failed validation: {}".format(exc.msg))
    response.status_int = 500
    return response


# pyramid.httpExceptions 里面还有一个 HTTFound 方法，他可以返回指定页面
def myview(request):
    return HTTPFound(location="http://www.baidu.com")


if __name__ == "__main__":
    pass
