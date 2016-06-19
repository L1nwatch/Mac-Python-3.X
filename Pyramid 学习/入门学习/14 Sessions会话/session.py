#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" session 相关知识
"""
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.config import Configurator
from pyramid.response import Response

__author__ = '__L1n__w@tch'


# 使用session对象
# 当你配置好 session factory 后, 你就可以通过 request 调用 session 对象了
# 我们可以像使用 python 字典一样使用 session 对象, 它支持所有字典操作方法, 除此之外还有其他一些额外属性和方法:
# 额外属性:
# created: session 创建时的时间戳
# new: boolean 型变量, 如果为 True 则这个 session 是新创建的, 否则是从其他已有的数据中产生的
#
# 额外的方法:
# changed(): 当你改变 session 名称空间里的可变变量时需要调用这个方法
# invalidate(): 设置 session 为无效
# 注意, session 中的数据必须是 pickleable 的, 也就是说里面的键值对必须是 python 的基本数据类型
# 如果 session 中有可变对象(比如 list 和字典), session 是不知道你改变了它的值的, 除非你调用 changed() 方法
# 所以，一旦你改变 session 中的数据, 最好是跟 changed() 说一声
def my_view(request):
    session = request.session
    if "abc" in session:
        session["fred"] = "yes"
    session["abc"] = "123"

    if "fred" in session:
        return Response("Fred was in the session")
    else:
        return Response("Fred was not in the session")


if __name__ == "__main__":
    # UnencryptedCookieSessionFactoryConfig, 这是在告诉你这个方法是默认的, 没有加密的工厂方法, 你不应该放一些敏感信息
    my_session_factory = UnencryptedCookieSessionFactoryConfig("???")

    config = Configurator(session_factory=my_session_factory)
