#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
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

        label_frame.grid(row=1, columnspan=1)
        frame.grid()

    def run(self):
        self.root_tk.title("ATM 平台 unicode_escape 编码转换")
        self.root_tk.resizable(height=False, width=False)

        self.set_button()

        self.set_text_label()

        self.root_tk.mainloop()

    def change_unicode(self):
        content = self.text_label.get(0.0, tkinter.END).replace("\\", "")

        readable_text = display_unicode(content)

        # 清空原有内容
        self.text_label.delete(0.0, tkinter.END)

        # 插入新的内容
        self.text_label.insert(0.0, readable_text)


def get_file_content():
    with codecs.open("test.txt", "r", encoding="utf8") as f:
        unicode_content = f.read().replace("\\", "")

    return unicode_content


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

    # with codecs.open("ok.txt", "w", encoding="utf8") as f:
    #     f.write(output)

    return output


if __name__ == "__main__":
    cc = CodingChange()
    cc.run()
