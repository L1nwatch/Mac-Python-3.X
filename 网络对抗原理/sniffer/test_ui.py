#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 测试 UI 用的, 要不然 sniff 和 UI 放在同一个文件不好测试
'''
__author__ = '__L1n__w@tch'

import tkinter
import threading
import time

test = list()


def test1():
    root = tkinter.Tk()

    frame = tkinter.Frame(root)

    label_frame = tkinter.LabelFrame(frame)
    labels = dict()
    # justify与anchor的区别了：一个用于控制多行的对齐；另一个用于控制整个文本块在Label中的位置
    labels["0"] = tkinter.Label(label_frame, text="AA", anchor="w", justify="left", width=20)
    labels["1"] = tkinter.Label(label_frame, text="BB", anchor="w", width=20)
    labels["2"] = tkinter.Label(label_frame, text="CC", anchor="w", width=20)
    labels["3"] = tkinter.Label(label_frame, text="DD", anchor="w", width=20)
    labels["4"] = tkinter.Label(label_frame, text="EE", anchor="w", width=20)

    for label in labels:
        labels[label].grid(row=0, column=int(label))

    label_frame.grid(row=0, columnspan=5)

    ## 包帧 Start
    packets_frame = tkinter.Frame(frame)
    ## 添加滚动条
    # listbox = tkinter.Listbox(frame, yscrollcommand=scrollbar.set)
    #
    listbox = tkinter.Listbox(packets_frame, width=100)
    scrollbar = tkinter.Scrollbar(packets_frame)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    listbox.bind('<Button-1>', print_list)

    t = threading.Thread(target=update, args=(listbox,))
    t.start()

    packets_frame.grid()
    ## 包帧 End

    frame.grid()
    root.mainloop()


def update(listbox):
    for i in range(30):
        data = "{:20}{:20}{:20}{:20}{:20}".format(str(i), "b", "c", "d", "e")

        listbox.insert(tkinter.END, data)
        listbox.pack(side=tkinter.LEFT, fill=tkinter.Y)
        listbox.yview(tkinter.END)
        # listbox.update_idletasks()
        time.sleep(0.1)


def test2():
    root = tkinter.Tk()

    left_top_frame = tkinter.LabelFrame(root)
    right_top_frame = tkinter.Frame(root)
    left_bottom_frame = tkinter.Frame(root)
    right_bottom_frame = tkinter.Frame(root)

    lt_text = tkinter.Text(left_top_frame, width=50)
    rt_text = tkinter.Text(right_top_frame, width=50)
    # lb_text = tkinter.Text(left_bottom_frame, width=50)
    # rb_text = tkinter.Text(right_bottom_frame, width=50)
    lt_text.pack()
    rt_text.pack()
    # lb_text.pack()
    # rb_text.pack()

    left_top_frame.grid(sticky=tkinter.W + tkinter.N)
    right_top_frame.grid(sticky=tkinter.E + tkinter.N)
    right_bottom_frame.grid(sticky=tkinter.E + tkinter.S)
    left_bottom_frame.grid(sticky=tkinter.W + tkinter.N)
    root.mainloop()


def print_list(event):
    print("aa")
    #     print(listbox.curselection()[0])
    pass


def test3():
    """
    用来测试多选框
    :return:
    """
    root = tkinter.Tk()

    checkbutton = tkinter.Checkbutton(root, text="aaa", command=lambda: print("aaa"))
    checkbutton.select()
    checkbutton.pack()
    checkbutton = tkinter.Checkbutton(root, text="bbb", command=lambda: print("bbb")).pack()
    checkbutton = tkinter.Checkbutton(root, text="ccc", command=lambda: print("ccc")).pack()
    checkbutton = tkinter.Checkbutton(root, text="ddd", command=lambda: print("ddd")).pack()

    root.mainloop()


if __name__ == "__main__":
    # test2()
    # test1()
    test3()
