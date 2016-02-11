#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 引入一些新元素和技术:
        ScrolledListBox 小部件
        如何捕捉底层事件,比如双击鼠标和窗口级别的事件
        如何创建和使用自定义对话框
        如何设置字体
        如何使用state属性激活/停用小部件
        如何使用面向对象的技术创建GUI
'''
__author__ = '__L1n__w@tch'

import tkinter.tix as tix
import tkinter.messagebox as mb
import optionsdialog as od
import lendydata as data
import os


class LendingLibrary:
    def __init__(self, root):
        self.is_dirty = False
        self.top = root
        root["menu"] = self.build_menus(root)
        main_win = self.build_notebook(root)
        main_win.pack(fill="both", expand=True)
        self.top.protocol("WM_DELETE_WINDOW", self.ev_close)
        self.top.title("Lending Libaray")
        data.init_db()  # use default file
        self.items = data.get_items()
        self.members = data.get_members()
        self.populate_item_list()
        self.populate_member_list()

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
        self.menu_bar = tix.Menu(top)
        for menu in menus:
            m = tix.Menu(top)
            for item in menu[1]:
                m.add_command(label=item[0], command=item[1])
            self.menu_bar.add_cascade(label=menu[0], menu=m)
        return self.menu_bar

    def build_notebook(self, top):
        mono_font = self.get_mono_font()
        nb = tix.NoteBook(top)

        nb.add("itam_page", label="items", raisecmd=lambda pg="item": self.ev_page(pg))
        fr = tix.Frame(nb.subwidget("item_page"))
        self.item_fmt = "{:15} {:15} {:10} ${:<8} {:12}"
        tix.Label(fr, font=mono_font,
                  text=self.item_fmt.format("Name", "Description", "Owner", "Price", "Condition")).pack(anchor="w")
        slb = tix.ScrolledListBox(fr, width=500, height=200)
        slb.pack(fill="both", expand=True)
        fr.pack(fill="both", expand=True)
        self.item_list = slb.subwidget("listbox")
        self.item_list.configure(font=mono_font, bg="white")
        self.item_list.bind("<Double-1>", self.ev_edit_item)

        nb.add("member_page", label="members", raisecmd=lambda pg="member": self.ev_page(pg))
        fr = tix.Frame(nb.subwidget("member_page"))
        self.member_fmt = "{:<15} {:<40}"
        tix.Label(fr, font=mono_font, text=self.member_fmt.format("Name", "Email Address")).pack(anchor="w")
        slb = tix.ScrolledListBox(fr, width=40, height=20)
        slb.pack(fill="both", expand=True)
        fr.pack(fill="both", expand=True)
        self.member_list = slb.subwidget("listbox")
        self.member_list.configure(font=mono_font, bg="white")
        self.member_list.bind("<Double-1>", self.ev_edit_member)

        return nb

    def get_mono_font(self):
        if os.name == "nt":
            return ("courier", "10", "")
        else:
            return ("mono", "10", "")

    def populate_item_list(self):
        self.item_list.delete("0", "end")
        for item in self.items:
            item = list(item[1:])
            item[2] = data.get_member_name(item[2])
            self.item_list.insert("end", self.item_fmt.format(*item))

    def populate_member_list(self):
        self.member_list.delete("0", "end")
        for mbr in self.members:
            self.member_list.insert("end", self.member_fmt.format(*mbr[1:]))

    def ev_close(self, event=None):
        data.close_db()
        self.top.quit()

    ##### notebook event handler #####
    def ev_page(self, page):
        if page == "item":
            self.menu_bar.entryconfigure("Item", state="active")
            self.menu_bar.entryconfigure("Member", state="disabled")
        if page == "member":
            self.menu_bar.entryconfigure("Item", state="disabled")
            self.menu_bar.entryconfigure("Member", state="active")

    ######### Item Event Handlers #######
    def ev_new_item(self):
        dlg = od.OptionsDialog(top, (
            ["Name", ""],
            ["Description", ""],
            ["Owner", ""],
            ["Price", ""],
            ["Condition", ""]
        ))

        if dlg.changed:
            owner_id = self.get_member_id(dlg.options[2][1])
            data.insert_item(dlg.options[0][1], dlg.options[1][1], owner_id, int(dlg.options[3][1]), dlg.options[4][1])
        self.items = data.get_items()
        self.populate_item_list()

    def ev_edit_item(self, event=None):
        # get selected member
        indices = self.item_list.curselection()
        index = int(indices[0]) if indices else 0
        item = self.items[index]
        owner_id = item[3]
        owner_name = data.get_member_name(owner_id)
        dlg = od.OptionsDialog(top, (
            ["Name", item[1]],
            ["Description", item[2]],
            ["Owner", owner_name],
            ["Price", item[4]],
            ["Condition", item[5]]))
        if dlg.changed:
            if dlg.options[2][1] != owner_name:  # its changed
                owner_id = self.get_member_id(dlg.options[2][1])
            data.update_item(item[0], dlg.options[0][1], dlg.options[1][1], owner_id, int(dlg.options[3][1]),
                             dlg.options[4][1])
            self.items = data.get_items()
            self.populate_item_list()

    def ev_delete_item(self):
        indices = self.item_list.curselection()
        index = int(indices[0]) if indices else 0
        item = self.items[index]
        data.delete_item(item[0])
        self.items = data.get_items()
        self.populate_item_list()

    # Ideally should use a combo box in options dialog.
    # this gives potential error if more than one member with same name
    def get_member_id(self, name):
        for member in self.members:
            if member[1] == name:
                return member[0]

    ######### Member Event Handlers #######
    def ev_new_member(self):
        dlg = od.OptionsDialog(top, (["Name", ""], ["Email", ""]))
        if dlg.changed:
            data.update_member(None, dlg.options[0][1], dlg.options[1][1])
            self.members = data.get_members()
            self.populate_member_list()

    def ev_edit_member(self, event=None):
        indices = self.member_list.curselection()
        index = int(indices[0]) if indices else 0
        mbr = self.members[index]
        dlg = od.OptionsDialog(top, (["Name", mbr[1]], ["Email", mbr[2]]))

        if dlg.changed:
            data.update_member(mbr[0], dlg.options[0][1], dlg.options[1][1])
            self.members = data.get_members()
            self.populate_member_list()

    def ev_delete_member(self):
        indices = self.member_list.curselection()
        index = int(indices[0]) if indices else 0
        mbr = self.members[index]
        data.delete_member(mbr[0])
        self.members = data.get_members()
        self.populate_member_list()

    #### Help event handler #
    def ev_help(self):
        mb.showinfo("Help", """
        Lending Library Application

        Item -> New: Create a new item in the library
        Item -> Edit: Modify the attributes of the selected item (default is first)
        Item -> Delete: Delete selected item (no default)

        Member -> New: Add a member to the library
        Member -> Edit: Modify selected members data
        Member -> Delete: Delete selected member (no default)

        Help -> Help: Display this screen
        Help -> About: About the program.""")


def main():
    global top
    top = tix.Tk()
    app = LendingLibrary(top)
    top.mainloop()


if __name__ == "__main__":
    main()
