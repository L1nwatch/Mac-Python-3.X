#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Mac下运行成功
'''
__author__ = '__L1n__w@tch'

import tkinter as tk
import tkinter.ttk as ttk


def main():
    top = tk.Tk()
    s = ttk.Style()
    # 需要将样式对象中的classic换成vista来获得Vista主题.需要小量额外的工作来定义样式对象.
    # 但除此之外,使用ttk基本上与普通Tkinter编程一样.当运行代码时,应该注意到按钮发生的改变不仅仅是外观上的简单调整
    # 例如,当鼠标移到按钮上时,他的颜色会发生变化
    s.theme_use("classic")
    tk.Button(top, text="old button").pack()
    ttk.Button(top, text="new button").pack()

    top.mainloop()


if __name__ == "__main__":
    main()
