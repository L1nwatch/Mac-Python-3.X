#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 会创建一个Config文件,可以将它应用于之前讨论的工具借用应用.这个Config文件描述了标准设置和任何特定用户的重写值.
这些设置仅限于借用期间(用天表示)和物品可以被借用的最大值(默认值是0,代表没有期限).
'''
__author__ = '__L1n__w@tch'

import configparser as cp


def main():
    conf = cp.ConfigParser()
    conf["DEFAULT"] = {"lending_period": 0, "max_value": 0}
    conf["Fred"] = {"max_value": 200}  # Fred's a bit rough with things!
    conf["Anne"] = {"lending_period": 30}  # She is a bit forgetful sometimes
    with open("toolhire.ini", "w") as toolhire:
        conf.write(toolhire)

    del (conf)  # get rid of the old one
    conf = cp.ConfigParser()  # create a new one
    conf.read("toolhire.ini")
    print(conf.sections())
    print(conf["DEFAULT"]["max_value"])
    print(conf["Anne"]["max_value"])
    print(conf["Anne"]["lending_period"])
    print(conf["Fred"]["max_value"])

    try:
        print(["Joe"])
    except KeyError as e:
        print("KeyError", e)

    print(conf.options("Anne"))  # 读取Anne可用的选项,发现解析器返回了默认值以及那些显式定义的值

    try:
        print(conf.options("DEFAULT"))  # options()对于DEFAULT部分并不可用,而需要使用显式的default()方法来获取那些选项
    except Exception as e:
        print(e)

    print(conf.defaults())


if __name__ == "__main__":
    main()
