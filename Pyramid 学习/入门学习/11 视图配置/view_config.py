#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 视图配置
"""
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.config import Configurator

__author__ = '__L1n__w@tch'


# view_config 用来修饰视图
# 这个视图用了三个限定词, 对应路由名为 ok, request 请求为 POST 方式, 并且具有 read 权限的外界请求
# 这里如果请求的用户没有 read 权限, 会返回一个 forbidden view
@view_config(route_name="ok", request_method="POST", permission="read")
def my_view(request):
    return Response("OK")


# 你也可以用 add_view() 来代替它
config = Configurator()
config.add_view("myPackage.views.my_view", route_name="ok", request_method="POST", permission="read")
# 如果你使用 @view_config, 那么你必须要使用 pyramid.config.Configurator 的 scan 方法
# 不然视图配置是不知道有这个东西的
config.scan()


# @view_config 有以下几种使用方式:
# 直接修饰函数
@view_config(route_name="edit")
def edit(request):
    return Response("edited!")


# 放在类声明的前面，修饰该类的 __call__ 方法
@view_config(route_name="hello")
class MyView:
    def __init__(self, request):
        self.request = request

    def __call__(self, *args, **kwargs):
        return Response("hello")


# 还有下面这种奇葩的使用方式(我想你在项目中肯定不会这样写的)
class MyView2:
    def __init__(self, request):
        self.request = request

    def __call__(self, *args, **kwargs):
        return Response("Hello2")


my_view2 = view_config(route_name="hello")(MyView2)


# 多个 view_config 修饰同一个函数, 这样路由 edit 和 change 都会调用 edit 函数
@view_config(route_name="edit")
@view_config(route_name="change")
def edit(request):
    return Response("edited!")


# 直接修饰类的方法
class MyView3:
    def __init__(self, request):
        self.request = request

    @view_config(route_name="hello3")
    def __call__(self, *args, **kwargs):
        return Response("Hello3")


# 修饰类的指定方法(比起这个, 更倾向上一种, 因为如果一个类有多个 view callable 的话, 写在每个类方法前面更清晰一些）
@view_config(attr="a_method", route_name="hello4")
class MyView3:
    def __init__(self, request):
        self.request = request

    def a_method(self):
        return Response("Hello4")


# 类修饰符 @view_defaults
# 类修饰符和 @view_config 配合使用非常方便. 对于一个类视图, 如果我们只用 @view_config, 就像这样:
class RESTView:
    def __init__(self, request):
        self.request = request

    @view_config(route_name="rest", request_method="GET")
    def get(self):
        return Response("get")

    @view_config(route_name="rest", request_method="POST")
    def post(self):
        return Response("post")

    @view_config(route_name="rest", request_method="DELETE")
    def delete(self):
        return Response("delete")


# 我们需要在每个方法前面都指定路由名, 如果他们都有公共的路由的话, 那这将做很多无用功. 如果使用类修饰符:
@view_defaults(route_name="rest")
class RESTView2:
    def __init__(self, request):
        self.request = request

    @view_config(request_method="GET")
    def get(self):
        return Response("get")

    @view_config(request_method="POST")
    def post(self):
        return Response("post")

    @view_config(request_method="DELETE")
    def delete(self):
        return Response("delete")


# 这样就不用在每个方法前都加一个 route_name. 如果再结合 match_param, 用起来会更方便
# 举个例子, 我们配置这样一个路由:
config.add_route("user", "/user/{action}")


# 这样写已经很清晰很规范了, 将与用户登录注册有关的视图都放在一个类里便于管理
@view_defaults(route_name="user")
class UserView:
    def __init__(self, request):
        self.request = request

    @view_config(renderer="user/regist.mako", match_param=("action=regist"), request_method="GET")
    def regist_get(self):
        return {}

    @view_config(renderer="jsonp", match_param=("action=regist"), request_method="POST")
    def regist_post(self):
        return {}

    @view_config(renderer="user/login.mako", match_param=("action=login"), request_method="GET")
    def login_get(self):
        return {}

    @view_config(renderer="jsonp", match_param=("action=login"), request_method="POST")
    def login_post(self):
        return {}


# HTTP 缓存
# 给 @view_config 添加 http_cache 参数可以设置缓存, 但在 request 请求中不想设置缓存怎么办呢?
# 你可以再代码中显示设定. 比如:
@view_config(http_cache=3600)
# 如果 request.params 中没有 should_cache 的话. 说明, 不用缓存
# 于是设置 response.cache_control.prevent_auto为True, 自动禁止缓存.
# 这里会将 @view_config 中的 http_cache 设置给覆盖掉
def view(request):
    response = Response()
    if "should_cache" not in request.params:
        response.cache_control.prevent_auto = True
    return response


if __name__ == "__main__":
    pass
