#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 了解的小部件包括ComboBox、ScrolledText和Notebook
直接在Mac下运行不了,好像是得安装tix组件?
'''
__author__ = '__L1n__w@tch'

import tkinter.tix as tix


def main():
    top = tix.Tk()
    lab = tix.Label(top)
    lab.pack()
    cb = tix.ComboBox(top, command=lambda s: lab.config(text=s))
    for s in ["Fred", "Ginger", "Gene", "Debbie"]:
        cb.insert("end", s)
    cb.pick(0)
    lab["text"] = "Pick any item"
    cb.pack()
    top.mainloop()


if __name__ == "__main__":
    main()
