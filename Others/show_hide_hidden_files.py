#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 本来已经用 automator 写了个显示隐藏文件和隐藏隐藏文件的 app了,但是我想再精简一下,而且提供更加可读的提示,
所以还是决定用 Python 写脚本后再用 automator 来运行

参考: http://www.conxz.net/blog/2013/10/25/sloppy-python-snippets-to-capture-command-output/
'''
__author__ = '__L1n__w@tch'

import subprocess
import tkinter.messagebox


def main():
    tk = tkinter.Tk()
    tk.withdraw()

    cmd = "defaults read com.apple.finder AppleShowAllFiles -boolean"
    popen = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE)
    res = popen.stdout.readline().strip()
    if res == b"1":
        subprocess.call("defaults write com.apple.finder AppleShowAllFiles -boolean false ; killall Finder", shell=True)
        tkinter.messagebox.showinfo("取消显示隐藏文件", "取消显示成功")
    elif res == b"0":
        subprocess.call("defaults write com.apple.finder AppleShowAllFiles -boolean true ; killall Finder", shell=True)
        tkinter.messagebox.showinfo("显示隐藏文件", "显示隐藏文件成功")
    else:
        tkinter.messagebox.showerror("Something wrong!")


if __name__ == "__main__":
    main()
