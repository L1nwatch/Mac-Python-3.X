#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 不返回 response, 则可以设立 renderer
"""
from pyramid.view import view_config
from pyramid.renderers import JSON
import datetime
from pyramid.renderers import JSONP
from pyramid.config import Configurator
from pyramid.response import Response

__author__ = '__L1n__w@tch'


# view callable 需要返回一个 response 对象, 其实也可以不用返回的.
# 当你不直接返回 response 时, Pyramid 会用 renderer 构建一个 response
@view_config(renderer="json")
def hello_world(request):
    # 这里返回了一个字典, pyramid 发现你没有返回 response 对象.
    # 于是就去 view_config 看你有没有配置 renderer
    # 这里是有的, 所以没有问题. 如果你不返回 response 也不设置 renderer, 就会报错.
    # 那如果既返回 response 对象又设置了 renderer 会怎么样呢? 答案是你的 renderer 白设了
    return {"content": "Json"}


# 使用渲染器(renderer)
# 渲染器可以是模板系统, 也可以是序列化的对象.
# 上面的 renderer = 'json' 用的就是对象. 你还可以用内置的 Chameleon 模板语言系统, 也可以用其他的, 比如 mako
@view_config(renderer="string")
def hello_world2(request):
    return {"content": "String"}


# 你可以自定义返回的对象. 方法是在相应的类里面创建一个 __json__ 方法, 接收 request 参数并返回 json 形式的值
class MyObject:
    def __init__(self, x):
        self.x = x

    def __json__(self, request):
        return {"x": self.x}


@view_config(renderer="json")
def objects(request):
    return [MyObject(1), MyObject(2)]


# 当然，你如果不这样做的话也可以创建自定义的JSON,并用适配器添加自定义类型：
"""
json_renderer = JSON()
# 这里我们创建了一个json_renderer实例，并用add_adapter方法添加了自定义类型。
def datetime_adapter(obj, request):
    return obj.isFormat()(iso?format?)
json_renderer.add_adapter(datetime.datetime, datetime_adapter)
"""

# jsonp
# pyramid.renderer.JSONP 实现了 json/jsonp 的混合渲染，所以项目中一般用 jsonp 渲染器
# 跟json一样，jsonp也可以用add_adapter方法创建自定义对象。
# 跟其他渲染器不同的是，jsonp渲染器需要手动添加到配置器里：
config = Configurator()
config.add_renderer("jsonp", JSONP(param_name="callback"))


# 添加之后才能使用
@view_config(renderer="jsonp")
def my_view(request):
    return {"content": "Jsonp"}


# Chameleon
# Chameleon 模板系统让你可以使用 *.pt, *.txt 文件作为渲染器
config.add_view("test", name="test", context="test", renderer="myProject:templates/test.pt")
config.add_view("test2", name="test2", context="test2", renderer="myProject:templates/test.pt")

# mako
# Mako 模板跟 Chameleon 模板差不多, 只不过后缀名是 mak 或者 mako
config.add_view("test3", name="test3", context="test3", renderer="test3.mak")


# 设置 Responses 的属性
# 如果在 view callable 里不返回 response 对象, 但又需要设置 response 的参数的时候, 你可以使用 request.response
# 比如你想设置返回的 response 的 status
@view_config(name="gone", renderer="templates/gone.pt")
def my_view2(request):
    request.response.status = "404 没找到"
    return {"URL": request.URL}


# 一旦你使用了 request.response, 你就不要再重新返回一个 Response 对象了.
# 下面这段代码中, 设置 cookie 是无效的
def my_view3(request):
    request.response.set_cookie("abc", "123")
    return Response("OK")


# 你应该这样:
def my_view4(request):
    request.response.set_cookie("abc", "123")
    return request.response


if __name__ == "__main__":
    pass
