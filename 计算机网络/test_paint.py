#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 需要画滑动窗口, 所以测试下怎么画好看

颜色的参考:
http://blog.csdn.net/gatieme/article/details/45439671
'''
__author__ = '__L1n__w@tch'

# /usr/bin/python
# -*- coding: utf-8 -*-


#   格式：\033[显示方式;前景色;背景色m

STYLE = {
    'fore':
        {  # 前景色
            'black': 30,  # 黑色
            'red': 31,  # 红色
            'green': 32,  # 绿色
            'yellow': 33,  # 黄色
            'blue': 34,  # 蓝色
            'purple': 35,  # 紫红色
            'cyan': 36,  # 青蓝色
            'white': 37,  # 白色
        },

    'back':
        {  # 背景
            'black': 40,  # 黑色
            'red': 41,  # 红色
            'green': 42,  # 绿色
            'yellow': 43,  # 黄色
            'blue': 44,  # 蓝色
            'purple': 45,  # 紫红色
            'cyan': 46,  # 青蓝色
            'white': 47,  # 白色
        },

    'mode':
        {  # 显示模式
            'mormal': 0,  # 终端默认设置
            'bold': 1,  # 高亮显示
            'underline': 4,  # 使用下划线
            'blink': 5,  # 闪烁
            'invert': 7,  # 反白显示
            'hide': 8,  # 不可见
        },

    'default':
        {
            'end': 0,
        },
}


def UseStyle(string, mode='', fore='', back=''):
    """
    学习网上的
    :param string: "要显示的字"
    :param mode: "bold"
    :param fore: "blue"
    :param back: "cyan"
    :return: "\033[1m测试显示模式\033[0m"
    """
    mode = "{}".format(STYLE['mode'][mode] if mode in STYLE['mode'] else '')
    fore = "{}".format(STYLE['fore'][fore] if fore in STYLE['fore'] else '')
    back = "{}".format(STYLE['back'][back] if back in STYLE['back'] else '')
    style = ';'.join([s for s in [mode, fore, back] if s])
    style = "\033[{}m".format(style if style else '')
    end = "\033[{}m".format(STYLE['default']['end'] if style else '')
    return '{}{}{}'.format(style, string, end)


def learning_color():
    print(UseStyle('高亮', mode='bold'), end=" ")
    print(UseStyle('下划线', mode='underline'), end=" ")
    print(UseStyle('闪烁', mode='blink'), end=" ")
    print(UseStyle('反白', mode='invert'), end=" ")
    print(UseStyle('不可见', mode='hide'), end=" ")
    print("")

    print("测试前景色")
    print(UseStyle('黑色', fore='black'), end=" ")
    print(UseStyle('红色', fore='red'), end=" ")
    print(UseStyle('绿色', fore='green'), end=" ")
    print(UseStyle('黄色', fore='yellow'), end=" ")
    print(UseStyle('蓝色', fore='blue'), end=" ")
    print(UseStyle('紫红色', fore='purple'), end=" ")
    print(UseStyle('青蓝色', fore='cyan'), end=" ")
    print(UseStyle('白色', fore='white'), end=" ")
    print("")

    print("测试背景色")
    print(UseStyle('黑色', back='black'), end=" ")
    print(UseStyle('红色', back='red'), end=" ")
    print(UseStyle('绿色', back='green'), end=" ")
    print(UseStyle('黄色', back='yellow'), end=" ")
    print(UseStyle('蓝色', back='blue'), end=" ")
    print(UseStyle('紫红色', back='purple'), end=" ")
    print(UseStyle('青蓝色', back='cyan'), end=" ")
    print(UseStyle('白色', back='white'), end=" ")
    print("")


if __name__ == "__main__":
    test1 = """
    ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
    │{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│{}│
    └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
    """

    # test2 = """
    # +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    # |{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|
    # +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    # """.format("00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "√ ", 11, 12, 13, 14, 15)

    buffer = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "√ ", 11, 12, 13, 14, 15]

    print(test1.format(*buffer))

    for i in range(0, 100):
        print("{}: \033[{}m测试显示模式\033[0m".format(i, i))

        # print(test2)
