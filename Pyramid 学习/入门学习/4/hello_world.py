#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 第一个 pyramid 程序
"""
# 跟其他Python web框架一样, Pyramid 用 WSGI 协议来将一个应用程序和web服务器联系到一起
# wsgiref 模块就是 WSGI 服务的一种封装，现在 wsgiref 已经被引入 Python 标准库了
from wsgiref.simple_server import make_server

# 引入了pyramid.config模块的Configurator类, 下面创建了它的一个实例，然后通过这个实例来配置我们的应用
from pyramid.config import Configurator

# pyramid.response.Response, 用来返回response信息
from pyramid.response import Response

__author__ = '__L1n__w@tch'


# View Callable 声明
#  一个视图调用接受一个参数:request. 它将返回一个 response 对象
# 一个 view callable 不一定是一个函数，也可以是一个类或一个实例
def hello_world(request):
    # 一个 view callable 总是伴随着调用 request 对象
    # 一个 request 对象就代表着一个通过被激活的 WSGI 服务器传送到 pyramid 的 HTTP 请求
    # 一个 view callable 还需要返回一个 response 对象
    # 因为一个 response 对象拥有所有来制定一个实际的 HTTP 响应所必要的信息
    # 这个对象通过 wsgi 服务器, 也就是 Pyramid, 转化为文本信息发送回请求的浏览器
    # 为了返回一个 response, 每个 view callable 创建一个 response 实例
    # 在 hello_world 函数中, 一个字符串作为 response 的 body 来返回
    return Response("Hello {}!".format(request.matchdict["test_name"]))


if __name__ == "__main__":
    # Application Configuration 应用程序配置
    # 创建了一个 Configuration 类的实例 config, 通过这个实例来对我们的 Pyramid 应用进行配置, 包括路由/ip/端口等信息
    # 调用 config 的各种方法设置应用程序注册表(application registry), 对我们的应用程序进行注册
    config = Configurator()
    # 调用 pyramid.config.Configurator.add_route() 方法, 注册了一个以 /hello/ 开头的 URL 路由, 路由的名字就叫 'hello'
    config.add_route("hello", "/hello/{test_name}")
    # 注册了一个 view callable 函数(也就是 hello_world 函数), 当名为 'hello' 的路由被匹配时应该调用这个函数
    config.add_view(hello_world, route_name="hello")

    '''
    这三者的对应关系也就是
        URL Path(比如 /hello/world ) ->
            route(比如 'hello' ) ->
                view callable(比如 hello_world 函数)
    这样, 一个前台页面就和一个后台处理方法对应起来了
    '''

    # WSGI Application Creation 创建 WSGI 应用程序
    # 当所有的配置工作完成后，python 脚本通过 pyramid.config.Configurator.make_wsgi_app() 方法来创建 WSGI 应用程序
    # 这个方法返回一个 WSGI 应用程序对象并传递给 app 引用，让 WSGI 服务器来使用
    app = config.make_wsgi_app()
    # WSGI 是一个让服务器能和 python 应用程序交流的协议
    # WSGI Application Serving
    # 我们启动了一个 WSGI 服务, make_server() 方法绑定了 ip 和端口
    # 最后一个参数传递我们的 app 对象(一个router), 也就是我们想服务的那个应用程序。
    server = make_server("localhost", 23330, app)
    # serve_forever() 方法创建了一个循环来接受外界的 request 请求
    server.serve_forever()
