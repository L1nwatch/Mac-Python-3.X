#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
# 先导入 numpy 和 matplotlib 模块，再利用 np.linspace 给定 x 值的范围，同时给予 y 函数赋值
"""
import numpy as np
import matplotlib.pyplot as plt  # 画图的 matlab 库

__author__ = '__L1n__w@tch'


def function(n):
    # 级数 sin(n*x)/n
    return np.sin(n * x) / n


def f(n):
    # 级数求和
    y = function(1)
    for i in range(2, n):
        y += function(i)
    return y


def fn(n):
    t = 0
    for i in range(1, n):
        t += f(i)
    return t


if __name__ == "__main__":
    # 设置 x 坐标轴, 从 -1 到 1 布置 1000 个单位
    x = np.linspace(-1, 1, 1000)

    # 画布设置
    plt.figure(figsize=(16, 8))

    n = [(40, "red"), (80, "black"), (160, "blue")]
    for i in n:
        t = fn(i[0])

        # 画图操作
        plt.plot(x, t / i[0], color=i[1], linewidth=2)

    # 显示操作
    plt.ylim(-3, 3)  # 设定 y 轴的范围
    plt.legend()
    plt.grid(True)  # 设置显示网格线
    plt.show()
