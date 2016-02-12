#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Mac OS X 10.10下测试logging模块
'''
__author__ = '__L1n__w@tch'

import logging


def test1():
    # 在使用任何日志方法前调用basicConfig()是很重要的.级别设置表明了信息显示的最低级别.
    # DEBUG是最低级别,所以所有内容都被打印了出来.除了设置级别,还可以指定一个输出文件名
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Heres some info")
    logging.error("Oops, thats bad")
    logging.critical("AAARGH, Its all gone wrong!")


def test2():
    # 也可以指定日志消息的格式,包括像消息日期、产生消息的文件和函数等这些消息(选项的相关文档都在日志文档的LogRecord部分)
    # 由于默认格式不包含任何日期或时间信息,因此常常希望进行一些设置:
    logging.basicConfig(format="%(asctime)s %(levelname)s : %(message)s")
    logging.error("Its going wrong")
    logging.critical("Told you...")


def test3():
    # 也可以在basicConfig()中使用datefmt参数,这样就可以使用与time.strftime()相同的选项来改变日期格式
    logging.basicConfig(format="%(levelname)s:%(asctime)s %(message)s", datefmt="%Y/%m/%d - %I : %M")
    logging.error("Its' happened again")


def main():
    # test1()
    # test2()
    test3()


if __name__ == "__main__":
    main()
