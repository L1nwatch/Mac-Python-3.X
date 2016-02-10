#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import tkinter as tk
import tkinter.messagebox as mb


def build_menu(parent):
    """
    菜单结构被定义为一组嵌套元组.叶节点菜单项包含了名称-函数对.
    然后创建顶层菜单栏对象并循环数据结构,创建了子菜单并将它们插入到菜单栏中,最后返回完整的菜单栏对象
    :param parent:
    :return:
    """
    global ev_new, ev_resume, ev_save, ev_exit, ev_help, ev_about
    menus = (("File", (("New", ev_new), ("Resume", ev_resume), ("Save", ev_save), ("Exit", ev_exit))),
             ("Help", (("Help", ev_help), ("About", ev_about))))
    menu_bar = tk.Menu(parent)
    for menu in menus:
        m = tk.Menu(parent)
        for item in menu[1]:
            m.add_command(label=item[0], command=item[1])
        menu_bar.add_cascade(label=menu[0], menu=m)

    return menu_bar


def dummy():
    """
    简单地定义一个虚拟函数(dummy function)来处理所有的事件
    :return:
    """
    mb.showinfo("Dummy", "Event to be done")


def main():
    global ev_new, ev_resume, ev_save, ev_exit, ev_help, ev_about

    top = tk.Tk()
    ev_new = dummy
    ev_resume = dummy
    ev_save = dummy
    ev_exit = top.quit
    ev_help = dummy
    ev_about = dummy

    m_bar = build_menu(top)
    top["menu"] = m_bar
    tk.mainloop()


if __name__ == "__main__":
    main()
