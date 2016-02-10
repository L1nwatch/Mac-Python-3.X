#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' tkinter示例代码
注意,示例中使用了一个用于小部件变量的命名约定.第一个字符表明了小部件的类型.
这有时作为每个变量类型的提醒器很有用,但是如果之后改变小部件的类型,就会产生维护的问题.使用这个命名约定是完全可选的
'''
__author__ = '__L1n__w@tch'

import tkinter as tk


def main():
    # create the event handler to clear the text
    def _ev_clear():
        nonlocal l_history, e_hello
        # 将l_history标签的文本设置为e_hello输入区域的内容,使用了字典风格的访问方式设置了标签的文本.这种技术也同样适用于小部件的任何属性
        l_history["text"] = e_hello.get()
        # delete()方法将0作为第一个参数,这表明文本的开始,而第二个参数是tk.END,他是一个特殊值,意味着文本的末端
        e_hello.delete(0, tk.END)

    # create the top level window/frame
    top = tk.Tk()

    # 创建了一个Frame来容器所有其他小部件
    F = tk.Frame(top)
    # 调用pack()触发了一个简单的布局管理器.在默认情况下,它只是自上向下地将组件封装到包含对象中.
    # fill选项告诉小部件在垂直和水平方向上扩展以充满窗口
    F.pack(fill="both")

    # 创建了第二个Frame来容纳Entry和Label小部件
    # Now the frame with text entry
    f_entry = tk.Frame(F, border=1)
    e_hello = tk.Entry(f_entry)
    e_hello.pack(side="left")
    l_history = tk.Label(f_entry, text=" ", foreground="steelblue")
    # 使用参数告诉包装器将小部件放在frame的旁边而不是默认地竖直堆积放置.
    l_history.pack(side="bottom", fill="x")
    f_entry.pack(side="top")

    # Finally the frame with the buttons.
    # sink this one for emphasis
    f_buttons = tk.Frame(F, relief="sunken", border=1)
    # 很重要的一点是,你只是指定了函数名,并没有使用名称后加圆括号的方式来调用它.这样做会将函数的返回值赋值为事件处理程序
    b_clear = tk.Button(f_buttons, text="clear text", command=_ev_clear)
    b_clear.pack(side="left", padx=5, pady=2)
    b_quit = tk.Button(f_buttons, text="quit", command=F.quit)
    b_quit.pack(side="left", padx=5, pady=2)
    f_buttons.pack(side="top", fill="x")

    # Now run the eventloop
    F.mainloop()


if __name__ == "__main__":
    main()
