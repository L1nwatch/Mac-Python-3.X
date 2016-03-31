#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 用于实现嗅探器的 UI 界面
'''
__author__ = '__L1n__w@tch'

import tkinter
import tkinter.ttk as ttk
import tkinter.messagebox as mb


class MySniff:
    def __init__(self, root):
        self.top = root
        self.top["menu"] = self.build_menus(root)

        self.ev_new_item = None
        self.ev_edit_item = None
        self.ev_delete_item = None
        self.ev_new_member = None
        self.ev_edit_member = None
        self.ev_delete_member = None
        self.ev_help = None

    def build_menus(self, top):
        menus = (("Item", (("New", self.ev_new_item),
                           ("Edit", self.ev_edit_item),
                           ("Delete", self.ev_delete_item),
                           )),
                 ("Member", (("New", self.ev_new_member),
                             ("Edit", self.ev_edit_member),
                             ("Delete", self.ev_delete_member),
                             )),
                 ("Help", (("Help", self.ev_help),
                           ("About", lambda: mb.showinfo(
                                   "Help About",
                                   "Lender application\nAuthor: Alan Gauld""")
                            ))))
        self.menu_bar = ttk.Menu(top)
        for menu in menus:
            m = tix.Menu(top)
            for item in menu[1]:
                m.add_command(label=item[0], command=item[1])
            self.menu_bar.add_cascade(label=menu[0], menu=m)
        return self.menu_bar


def main():
    root = tkinter.Tk()

    # 菜单栏


    # 功能实现区
    # 列表帧
    # IP 列表区域
    # 包 列表

    # 内容显示帧
    # 图形化显示/其余功能选项帧
    # 内容显示帧


    root.mainloop()


if __name__ == "__main__":
    main()
