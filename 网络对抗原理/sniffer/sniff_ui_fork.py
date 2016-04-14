#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
'''
多进程版本,发现不太好共享变量,所以还是全部改写成多线程好了

用于实现嗅探器的 UI 界面, 本来想用 PyQt 写的, 但是还没学, 而且时间不够, 所以还是用 tkinter 实现了
'''
__author__ = '__L1n__w@tch'

import os
import threading
import tkinter
from collections import OrderedDict

from submit.my_sniffer import MySniffer


class MyUI:
    def __init__(self):
        global l_packets

        self.my_sniffer = MySniffer()
        pid = os.fork()

        # 注意利用 fork 创建多进程只适用于 Unix/Linux/Mac, windows 用 multiprocessing
        # child process(sniffer)
        if pid == 0:
            self.l_packets = l_packets
            self.my_sniffer.sniff()
        else:
            ### 主窗口
            self.root = tkinter.Tk()
            self._initialize_root(self.root)

            # 输入控件
            # v = tkinter.StringVar()
            # enter = tkinter.Entry(self.root, textvariable=v, bg="yellow", width=80)
            # enter.grid()

            ## 菜单栏
            menu_frame = tkinter.Frame(self.root)
            self._initialize_menu(menu_frame)

            ## 功能实现区
            # 列表帧, 包括 IP 列表区域, 包列表区域
            packets_frame = tkinter.Frame(self.root)
            self._initialize_list_frame(packets_frame)

            # 内容显示帧, 包括图形化显示/其余功能选项区域, 内容显示区域
            content_frame = tkinter.Frame(self.root)
            self._initialize_content_frame(content_frame)

            ## 状态栏
            # state_frame = tkinter.Frame(self.root)

            self.root.mainloop()

    def _update_packets_list(self, listbox):
        for i in range(10000):
            for each in self.l_packets:
                print(each)
                listbox.insert(0, each)
                listbox.update_idletasks()

    def _initialize_menu(self, frame):
        buttons = OrderedDict()

        # 创建各种按钮
        buttons["start"] = tkinter.Button(frame, text="Start capturing packets", fg="red", command=None)
        buttons["stop"] = tkinter.Button(frame, text="Stop capturing packets", fg="blue", command=None)
        buttons["restart"] = tkinter.Button(frame, text="Restart current capture", fg="orange", command=None)
        buttons["options"] = tkinter.Button(frame, text="Capture options", fg="green", command=None)

        # 放置控件
        column = 0
        for each_button in buttons:
            buttons[each_button].grid(row=0, column=column)
            column += 1
        frame.grid(row=0)

    def _initialize_root(self, root):
        # 设置窗口大小
        root.geometry("800x640")

        # 设置标题
        root.title("Sniffer By w@tch")

        # 不允许更改窗口大小
        root.resizable(height=False, width=False)

    def _initialize_content_frame(self, frame):
        # 图形化显示/其余功能选项帧
        functions_listbox = tkinter.Listbox(frame)
        functions_listbox.grid(sticky=tkinter.W, row=0, column=0)

        # 内容显示帧
        content_label_frame = tkinter.LabelFrame(frame)
        contents_text = tkinter.Text(content_label_frame)

        contents_text.insert(tkinter.END, "Aaa")

        contents_text.grid()
        content_label_frame.grid(sticky=tkinter.E, row=0, column=1)

        frame.grid()

    def _initialize_list_frame(self, frame):
        # IP 列表区域
        ip_list_box = tkinter.Listbox(frame)
        ip_list_box.grid(row=0, column=0)

        # 包 列表
        packets_list_box = tkinter.Listbox(frame)

        packets_update_thread = threading.Thread(target=self._update_packets_list, args=(packets_list_box,))
        packets_update_thread.start()

        packets_list_box.grid(row=0, column=1)
        frame.grid()


if __name__ == "__main__":
    ui = MyUI()
