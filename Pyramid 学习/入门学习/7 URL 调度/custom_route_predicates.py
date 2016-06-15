#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 自定义参数?
"""
from pyramid.config import Configurator

__author__ = '__L1n__w@tch'


# 在这里，any_of 函数产生了一个 predicate, 保证匹配到的 url 值在 allowed 元组里面.
# 这里的 url 值保存在 segment_name 里，而 *allowed 就是保存允许值的元组 ('one', 'two', 'three')
# 所以只有当你输入的路径为 /one, /two 或者 /three 时 any_of 函数才会返回 True
def any_of(segment_name, *allowed):
    # predicate callable 具有以下条件：必须传入两个参数。
    # 第一个是字典，通常取名 info. info有一个 match 键, 这个键保存匹配到的 URL 参数信息
    # 第二个参数就是 request 对象
    def predicate(info, request):
        if info["match"][segment_name] in allowed:
            return True

    return predicate


def twenty_ten(info, request):
    # info 字典里面还有一个 route 对象, route 对象有两个很有用的属性: name 和 pattern
    # name 是路由的名字, pattern 就是 route pattern
    if info["route"].name in ("ymd", "ym", "y"):
        # 这个 predicate 的功能就是确保路由名为 y，ym，ymd 的路由所匹配到的年份 year 必须是 2010 年
        return info["match"]["year"] == "2010"


# ================= Start =====================
# 如果predicate是一个类的话，需要添加__text__属性。
class DummyCustomPredicate1:
    def __init__(self):
        self.__text__ = "my custom class predicate"


class DummpyCustomPredicate2:
    __text__ = "my custom class predicate"
# ================= End =====================


# ================= Start =====================
# 如果是函数，你需要在函数声明后为它设定一个__text__:
def custom_predicate():
    pass


custom_predicate.__text__ = "my custom method predicate"
# ================= End =====================


# ================= Start =====================
# 如果是类方法的话，你需要调用 classmethod 方法：
def classmethod_predicate():
    pass


classmethod_predicate.__text__ = "my custom method predicate"
classmethod_predicate = classmethod(classmethod_predicate)
# 当然，如果是静态方法的话把 classmethod 换成 staticmethod 就行了
# ================= End =====================


if __name__ == "__main__":
    num_one_two_or_three = any_of("num", "one", "two", "three")

    config = Configurator()
    # 为 add_route 方法添加了 custom_predicates 参数，并且传入 num_one_two_or_three 参数(any_of 函数)
    # any_of -> predicate callable
    config.add_route("route_to_num", "/{num}", custom_predicates=(num_one_two_or_three,))

    config.add_route("y", "/{year}", custom_predicates=(twenty_ten,))
    config.add_route("ym", "/{year}/{month}", custom_predicates=(twenty_ten,))
    config.add_route("ymd", "/{year}/{month}/{day}", custom_predicates=(twenty_ten,))
