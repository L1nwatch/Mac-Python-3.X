#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import tkinter.messagebox as mb
import tkinter as tk
import oxo_menu


def ev_click(row, col):
    mb.showinfo("Cell clicked", "row:{}, col:{}".format(row, col))


def build_board(parent):
    outer = tk.Frame(parent, border=2, relief="sunken")
    inner = tk.Frame(outer)
    inner.pack()

    # 使用网格布局管理器而不是封装器,因为面板布局完美地匹配网格布局风格
    for row in range(3):
        for col in range(3):
            cell = tk.Button(inner, text=" ", width="5", height="2", command=lambda r=row, c=col: ev_click(r, c))
            cell.grid(row=row, column=col)
    return outer


def main():
    top = tk.Tk()
    m_bar = oxo_menu.build_menu(top)
    top["menu"] = m_bar

    board = build_board(top)
    board.pack()
    status = tk.Label(top, text="testing", border=0, background="lightgrey", foreground="red")
    status.pack(anchor="s", fill="x", expand=True)

    tk.mainloop()


if __name__ == "__main__":
    main()
