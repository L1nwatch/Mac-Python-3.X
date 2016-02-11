#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 最后一个要熟悉的小部件是NoteBook小部件。它更加复杂，包含一些页。每页都有一个相关的标签。用户可以选择标签来激活相关的页。
页只是一个Tkinter容器。可以使用任何控件来填充它。通常，它是一个文本窗口或窗体。

以下将会创建一个两页的notebook。第一页包含一个ScrolledText小部件，而另一页包含一组用于启动各种消息对话框的按钮。
'''
__author__ = '__L1n__w@tch'

import tkinter.tix as tix
import tkinter.messagebox as mb


def main():
    top = tix.Tk()

    nb = tix.NoteBook(top, width=300, height=200)
    nb.pack(expand=True, fill="both")

    nb.add("page1", label="text")
    f1 = tix.Frame(nb.subwidget("page1"))
    st = tix.ScrolledText(f1)
    st.subwidget("text").insert("1.0", "Here is where the text goes...")
    st.pack(expand=True)
    f1.pack()

    nb.add("page2", label="Message Boxes")
    f2 = tix.Frame(nb.subwidget("page2"))
    # 通过联合使用expand,fill和anchor，在窗口大小改变时，可以精确地控制小部件的行为
    tix.Button(f2, text="error", bg="lightblue", command=lambda t="error", m="This is bad!": mb.showerror(t, m)).pack(fill="x",
                                                                                                                      expand=True)
    tix.Button(f2, text="info", bg="pink", command=lambda t="info", m="Information": mb.showinfo(t, m)).pack(fill="x", expand=True)
    tix.Button(f2, text="warning", bg="yellow", command=lambda t="warning", m="Don't do it!": mb.showwarning(t, m)).pack(fill="x",
                                                                                                                         expand=True)
    tix.Button(f2, text="question", bg="green", command=lambda t="question", m="Will I?": mb.askquestion(t, m)).pack(fill="x",
                                                                                                                     expand=True)
    tix.Button(f2, text="yes - no", bg="lightgrey", command=lambda t="yes - no", m="Are you sure?": mb.askyesno(t, m)).pack(
            fill="x", expand=True)
    tix.Button(f2, text="yes - no - cancel", bg="black", fg="white",
               command=lambda t="yes - not - cancel", m="Last chance...": mb.askyesnocancel(t, m)).pack(fill="x", expand=True)

    f2.pack(side="top", fill="x")
    top.mainloop()


if __name__ == "__main__":
    main()
