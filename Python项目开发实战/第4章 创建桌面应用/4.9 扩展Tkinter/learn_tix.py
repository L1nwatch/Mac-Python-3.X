#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 了解的小部件包括ComboBox、ScrolledText和Notebook
直接在Mac下运行不了,好像是得安装tix组件?
Mac 参考:http://stackoverflow.com/questions/27751923/tkinter-tclerror-cant-find-package-tix
说是tix已经落伍了,推荐使用Ttk,所以这个在Mac下运行不了我也不去解决了
Windows下运行成功了
'''
__author__ = '__L1n__w@tch'

import tkinter.tix as tix


def test1():
    top = tix.Tk()
    lab = tix.Label(top)
    lab.pack()
    # 使用的是config()而不是之前使用的字典来设置文本属性。事件处理程序lambda函数使用了字符串参数s
    # 它是通过小部件事件传入的。字符串保存当前选择的值
    cb = tix.ComboBox(top, command=lambda s: lab.config(text=s))
    for s in ["Fred", "Ginger", "Gene", "Debbie"]:
        cb.insert("end", s)
    cb.pick(0)
    lab["text"] = "Pick any item"
    cb.pack()
    top.mainloop()


def test2():
    top = tix.Tk()
    # ScrolledText小部件是标准Text小部件的扩展，它可以显示图片以及格式化的文本。tix版本的ScrolledText小部件
    # 自动添加了滚动条，使用标准工具包来实现这一功能会产生很大的工作量。在使用方法上，它与其他Tkinter小部件非常相似
    # 注意，虽然所有文本都显示在Tix的scrolledText小部件中，但是实际上使用了底层的标准Tkinter Text小部件来处理文本
    st = tix.ScrolledText(top, width=300, height=100)
    st.pack(side="left")

    # 可以手动在文本框中输入或以编程的方式插入文本
    # 使用了subwidget()方法来获得底层文本小部件的一个引用，然后使用它的insert()方法插入文本。
    t = st.subwidget("text")
    t.insert("0.0", "Some inserted text")
    t.insert("end", "\n more inserted text")

    # 也可以在文本小部件中选中文本区域
    # tag_configure()方法新建了一个tag，也就是文本的标签。标签被称为newfont并使用加粗的16号Roman字体。
    # 在Tkinter中，这是标准的三字体说明符格式（因此Tix和ttk也支持）
    t.tag_configure("newfont", font=("Roman", 16, "bold"))
    # 注意：Tkinter中的文本索引使用包含格式化成浮点数的字符串。但实际上，它包含了用点分隔的行和列坐标。行开始于1，但列开始于0.
    # 所以1.0是第一行的第一个字符。可以使用字符串end或预定义的常量tkinter.END来标识行的结束，或者所有文本的结束。
    s = t.get("1.0", "1.end")
    t.delete("1.0", "1.end")
    t.insert("1.0", s, "newfont")

    top.mainloop()


def main():
    # test1()
    test2()


if __name__ == "__main__":
    main()
