#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 用于实现嗅探器的 UI 界面, 本来想用 PyQt 写的, 但是还没学, 而且时间不够, 所以还是用 tkinter 实现了
'''
__author__ = '__L1n__w@tch'

import tkinter
import tkinter.messagebox as mb
from collections import OrderedDict


class MySniff:
    pass


def initialize_menu(frame):
    buttons = OrderedDict()

    # 创建各种按钮
    buttons["start"] = tkinter.Button(frame, text="Start capturing packets", fg="red", command=None)
    buttons["stop"] = tkinter.Button(frame, text="Stop capturing packets", command=None)
    buttons["restart"] = tkinter.Button(frame, text="Restart current capture", command=None)
    buttons["options"] = tkinter.Button(frame, text="Capture options", command=None)

    # 放置控件
    column = 0
    for each_button in buttons:
        buttons[each_button].grid(row=0, column=column)
        column += 1
    frame.grid(row=0)


def initialize_root(root):
    # 设置窗口大小
    root.geometry("800x640")

    # 设置标题
    root.title("Sniffer By w@tch")

    # 不允许更改窗口大小
    root.resizable(height=False, width=False)


def initialize_content_frame(frame):
    # 图形化显示/其余功能选项帧
    # 内容显示帧
    pass


def initialize_list_frame(frame):
    # IP 列表区域
    ip_list_box = tkinter.Listbox(frame)
    ip_list_box.grid(row=0, column=0)

    # 包 列表
    packets_list_box = tkinter.Listbox(frame)
    packets_list_box.grid(row=0, column=1)

    frame.grid()


if __name__ == "__main__":
    ### 主窗口
    root = tkinter.Tk()
    initialize_root(root)

    # 输入控件
    # v = tkinter.StringVar()
    # enter = tkinter.Entry(root, textvariable=v, bg="yellow", width=80)
    # enter.grid()

    ## 菜单栏
    menu_frame = tkinter.Frame(root)
    initialize_menu(menu_frame)

    ## 功能实现区
    packets_frame = tkinter.Frame(root)
    # 列表帧, 包括 IP 列表区域, 包列表区域
    initialize_list_frame(packets_frame)

    # 内容显示帧, 包括图形化显示/其余功能选项区域, 内容显示区域
    content_frame = tkinter.Frame(root)
    initialize_content_frame(content_frame)

    ## 状态栏
    state_frame = tkinter.Frame(root)

    root.mainloop()
