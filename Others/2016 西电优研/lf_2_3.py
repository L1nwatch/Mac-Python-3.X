#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
先导入 numpy 和 matplotlib 模块，再利用 np.linspace 给定 x 值的范围，同时给予 y 函数赋值
"""
import numpy as np
import matplotlib.pyplot as plt  # 画图的 matlab 库

__author__ = '__L1n__w@tch'


def function(n):
    # 级数 sin(n*x)/n
    return np.sin(n * x) / n


if __name__ == "__main__":
    x = np.linspace(-1, 1, 1000)
    y = function(1)

    # 画布设置
    plt.figure(figsize=(16, 8))

    for i in range(2, 200):
        # 画图操作
        plt.plot(x, y, color="blue", linewidth=2)
        # 级数求和
        y += function(i)

    # 画图操作
    plt.plot(x, y, color='red', linewidth=2)
    plt.ylim(-2, 2)
    plt.legend()
    plt.grid(True)
    plt.show()
