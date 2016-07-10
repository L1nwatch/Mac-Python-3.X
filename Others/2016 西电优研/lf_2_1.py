#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
先导入 numpy 和 matplotlib 模块，再利用 np.linspace 给定 x 值的范围，同时给予 y 函数赋值
"""
import numpy as np
import matplotlib.pyplot as plt  # 画图的 matlab 库

__author__ = '__L1n__w@tch'


def E():
    def f(n):
        # 级数 sin(n*x)/n
        return np.sin(n * x) / n

    y = f(1)
    # 级数求和
    for i in range(2, 200):
        y += f(i)
    return y


if __name__ == "__main__":
    # x 值和 y 值设定
    x = np.linspace(0, 20, 1000)  # 设置 x 坐标轴, 从 0 到 20 布置 1000 个单位
    y = E()  # 对 y 进行相应求值

    # 画图操作
    plt.figure(figsize=(16, 8))  # 设定画布大小
    plt.plot(x, y, color='red', linewidth=2)  # 瞄点
    plt.ylim(-2, 2)
    plt.legend()
    plt.grid(True)
    plt.show()
