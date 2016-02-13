#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 以下这个画布小程序显示了一个红圈
'''
__author__ = '__L1n__w@tch'

import tkinter as tk


def main():
    top = tk.Tk()
    c = tk.Canvas(top, width=50, height=50)
    c.pack()
    c.create_oval(10, 10, 40, 40, outline="red", fill="red")
    top.mainloop()


if __name__ == "__main__":
    main()
