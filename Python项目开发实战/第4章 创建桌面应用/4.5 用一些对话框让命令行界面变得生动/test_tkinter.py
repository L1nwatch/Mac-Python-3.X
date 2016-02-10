#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import tkinter.messagebox as mb
import tkinter


def main():
    # 为了不让空窗口出现,必须导入主Tkinter模块并实例化顶层Tk对象.然后通过调用withdraw()让对象不可见
    tk = tkinter.Tk()
    tk.withdraw()  # 去掉空窗口

    print(dir(mb))

    # 注意,一些函数返回字符串,比如ok,而其他函数则返回布尔结果.最好在交互式提示符上实验它们,以便知道返回值的类型.
    # 注意,当出现Cancel时,单击它会返回None
    mb.showinfo("Title", "Your message here")
    mb.showerror("An Error", "Oops!")
    mb.showwarning("Title", "This may not work...")
    mb.askyesno("Title", "Do you love me?")
    mb.askokcancel("Title", "Are you well?")
    mb.askquestion("Title", "How are you?")
    mb.askretrycancel("Title", "Go again?")
    mb.askyesnocancel("Title", "Are you well?")


if __name__ == "__main__":
    main()
