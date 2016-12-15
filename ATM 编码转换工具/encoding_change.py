#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.15 给 cl 试了之后发现没有右键功能, 果断添加
2016.12.15 Windows 下经常遇到前台编码显示不正常的问题, 于是需要通过编码工具转换一下
"""
import tkinter
import codecs
import re

__author__ = '__L1n__w@tch'


class CodingChange:
    def __init__(self):
        self.root_tk = tkinter.Tk()
        self.text_label = None

        # tear-off设置成0就不会有开头的虚线，也不会让你的菜单可以单独成为窗口
        self.menu = None

    def set_button(self):
        """
        设置一个点击按钮, 点击后读取文本然后进行转换的
        :return:
        """
        frame = tkinter.Frame(self.root_tk)
        label_frame = tkinter.LabelFrame(frame)
        button = tkinter.Button(label_frame, text="点击转换编码", command=lambda: self.change_unicode())
        button.grid()
        label_frame.grid(row=0, columnspan=1)
        frame.grid()

    def set_text_label(self):
        """
        设置一个可以输入输出的文本框
        :return:
        """
        frame = tkinter.Frame(self.root_tk)
        label_frame = tkinter.LabelFrame(frame)

        self.text_label = tkinter.Text(label_frame, width=60, height=40)
        self.text_label.grid()

        # 绑定右键单击事件到用来传递事件的函数, 注意 mac 右键居然是 button-2, 而 windows 下右键是 button-3
        self.text_label.bind("<Button-3>", self.right_menu_popup)
        # 绑定事件
        self.text_label.bind("<Control-Key-a>", self.__select_all_text)
        self.text_label.bind("<Control-Key-A>", self.__select_all_text)

        # 文本框-竖向滚动条
        text_label_scroll_bar = tkinter.Scrollbar(self.text_label, orient=tkinter.VERTICAL)
        # 滚动事件
        text_label_scroll_bar.config(command=self.text_label.yview)

        # self.text_label.config(command=self.text_label.xview)

        label_frame.grid(row=1, columnspan=1)
        frame.grid()

    def set_root(self):
        """
        设置有关主窗体的配置
        :return:
        """
        self.root_tk.title("ATM 平台 unicode_escape 编码转换")
        # self.root_tk.geometry('640x360')  # 设置了主窗口的初始大小960x540 800x450 640x360
        self.root_tk.resizable(height=False, width=False)
        self.root_tk.iconbitmap('bitbug_favicon.ico')

    def right_menu_popup(self, event):
        # 添加三个按钮，command设置回调函数
        # menu.add_separator 用来设置每个菜单按钮之间的间隔符（横线）
        if not self.menu:
            self.menu = tkinter.Menu(self.text_label, tearoff=0)
            self.menu.add_command(label="复制全部", command=self.on_copy)
            self.menu.add_separator()
            self.menu.add_command(label="从剪切板进行粘贴", command=self.on_paste)
            self.menu.add_separator()
            self.menu.add_command(label="剪切全部", command=self.on_cut)
        self.menu.tk_popup(event.x_root, event.y_root)

    def run(self):
        self.set_root()
        self.set_button()
        self.set_text_label()

        self.root_tk.mainloop()

    def change_unicode(self):
        content = self.text_label.get(0.0, tkinter.END).replace("\\", "")

        readable_text = display_unicode(content)

        # 清空原有内容
        self.__clear_text()

        # 插入新的内容
        self.text_label.insert(0.0, readable_text)

    def __clear_text(self):
        """
        清空 text
        :return:
        """
        self.text_label.delete(0.0, tkinter.END)

    def __select_all_text(self, event):
        """
        文本全选
        :return:
        """
        self.text_label.tag_add(tkinter.SEL, "1.0", tkinter.END)
        return 'break'  # 为什么要return 'break'

    def on_paste(self):
        """
        # 粘贴的回调函数
        :return:
        """
        content_from_system = str()

        try:
            # 获得系统粘贴板内容
            content_from_system = self.root_tk.clipboard_get()

        except tkinter.TclError:
            # 防止因为粘贴板没有内容报错
            pass

        # 在文本框中设置刚刚获得的内容
        self.text_label.insert(0.0, content_from_system)

    def on_copy(self):
        """
        # 复制的回调函数
        :return:
        """
        # 获得文本框内容
        content_from_text = self.text_label.get(0.0, tkinter.END)

        # 添加至系统粘贴板
        self.root_tk.clipboard_append(content_from_text)

    def on_cut(self):
        """
        # 剪切的回调函数
        :return:
        """
        self.on_copy()  # 前面步骤与复制相同，所以可以直接调用复制的函数

        try:
            # 删除文本框中从第一个到最后一个字符
            self.__clear_text()
        except tkinter.TclError:
            pass


def display_unicode(unreadable_content):
    unicode_dic = {}

    regex = "u\{\w{4}\}"

    regex_res = re.findall(regex, unreadable_content)

    for each in regex_res:
        test = r"\u" + each.replace("u{", "").replace("}", "")
        unicode_dic[each] = test.encode("utf8").decode("unicode_escape")

    output = unreadable_content
    for each_key in unicode_dic:
        output = output.replace(each_key, unicode_dic[each_key])

    return output


if __name__ == "__main__":
    cc = CodingChange()
    cc.run()
