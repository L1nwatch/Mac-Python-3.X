#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 参考 http://pyramidoc.lofter.com/post/386b18_1150b32
'''
__author__ = '__L1n__w@tch'

from pyramid.response import Response
from pyramid.config import Configurator

# 单文件应用 - 创建第一个 Pyramid 学习
# 访问: http://localhost:12309/hello/test
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    return Response("Hello {}!".format(request.matchdict["name"]))
    # return Response("Hello %(name)s!" % request.matchdict)


if __name__ == "__main__":
    config = Configurator()
    config.add_route("hello", "/hello/{name}")
    config.add_view(hello_world, route_name="hello")
    app = config.make_wsgi_app()
    server = make_server("0.0.0.0", 12309, app)
    server.serve_forever()

"""
# 冗长
config = Configurator()
config.add_route("xhr_route", "/xhr/{id}")
config.add_view("my.package.GET_view", route_name="xhr_route", xhr=True, permission="view", request_method="GET")
config.add_view("my.package.POST_view", route_name="xhr_route", xhr=True, permission="view", request_method="POST")
config.add_view("my.package.HEAD_view", route_name="xhr_route", xhr=True, permission="view", request_method="HEAD")


# 精简
def add_protected_xhr_views(config, module):
    module = config.maybe_dotted(module)
    for method in ("GET", "POST", "HAED"):
        view = getattr(module, "xhr_%s_view" % method, None)
        if view is not None:
            config.add_view(view, route_name="xhr_route", xhr=True, permission="view", request_method=method)


config = Configurator()
config.add_directive("add_protected_xhr_views", add_protected_xhr_views)

config.add_route("xhr_route", "/xhr/{id}")
config.add_protected_xhr_views("my.package")
"""

"""
# “Global”响应对象
def aview(request):
    response = request.response
    response.body = "Hello World!"
    response.content_type= "text/plain"
    return response
"""

"""
# 视图响应适配器
from pyramid.config import Configurator
from pyramid.response import Response


def tuple_response_adapter(val):
    status_int, content_type, body = val
    response = Response(body)
    response.content_type = content_type
    response.status_int = status_int
    return response


def string_response_adapter(body):
    response = Response(body)
    response.content_type = "text/html"
    response.status_int = 200
    return response


if __name__ == "__main__":
    config = Configurator()
    config.add_response_adapter(string_response_adapter, str)
    config.add_response_adapter(tuple_response_adapter, tuple)


def aview(request):
    return "Hello World!"


def another_view(request):
    return (403, "text/plain", "Forbidden")
"""

"""
# 视图响应适配器
from pyramid.config import Configurator
from pyramid.response import Response


def string_response_adapter(s):
    response = Response(s)
    response.content_type = "text/html"
    return response


if __name__ == "__main__":
    config = Configurator()
    config.add_response_adapter(string_response_adapter, str)
"""

"""
# 配置的可扩展性
from pyramid.config import Configurator

if __name__ == "__main__":
    config = Configurator()
    config.include("pyramid_jin_ja2")
    config.include("pyramid_exc_log")
    config.include("some.other.gus.package", route_prefix="/some_other_guy")
"""

"""
# 在视图渲染器中返回字典
from pyramid.renderers import render_to_response
from pyramid.view import view_config


# 被替代的
def myview(request):
    return render_to_response("myapp:templates/mytemplate.pt", {"a": 1}, request=request)

# 替代上面的一种写法
@view_config(renderer="myapp:templates/mytemplate.pt")
def myview(request):
    return {"a": 1}
"""

"""
# 几个作为类里面的方法定义的 view callable
from pyramid.view import view_config
from pyramid.response import Response


class AView(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name="view_one")
    def view_one(self):
        return Response("one")

    @view_config(route_name="view_two")
    def view_two(self):
        return Response("two")
"""

"""
# 基于修饰符的配置
from pyramid.view import view_config
from pyramid.response import Response


@view_config(route_name="fred")
def fred_view(request):
    return Response("fred")
"""
