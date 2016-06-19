#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 模板系统相关介绍
"""
from pyramid.renderers import render_to_response
from pyramid.renderers import render
from pyramid.response import Response
from mako.template import Template

__author__ = '__L1n__w@tch'


# 直接使用模板
def sample_view(request):
    # 通过调用 render_to_response 方法
    # 第一个参数是使用的模板文件, 第二个是传入模板的数据字典, 第三个是 request 对象
    return render_to_response("templates/foo.pt", {"foo": 1, "bar": 2}, request=request)


# 你还可以这样:
def sample_view2(request):
    result = render("myPackage:templates/foo.pt", {"foo": 1, "bar": 2}, request=request)
    response = Response(result)
    return response


# 或者这样:
def make_view(request):
    template = Template(filename="/templates/template.mak")
    result = template.render(name=request.params["name"])
    response = Response(result)
    return response


# 又或者这样:
def sample_view3(request):
    response = render_to_response("templates/foo.pt", {"foo": 1, "bar": 2}, request=request)
    response.content_type = "text/plain"
    response.status_int = 204
    return response


# 还可以这样:
def sample_view4(request):
    result = render("mypackage:templates/foo.pt", {"foo": 1, "bar": 2}, request=request)
    response = Response(result)
    response.content_type = "text/plain"
    return response


if __name__ == "__main__":
    pass
