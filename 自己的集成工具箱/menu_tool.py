#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 本来已经用 automator 写了个显示隐藏文件和隐藏隐藏文件的 app了,但是我想再精简一下,而且提供更加可读的提示,
所以还是决定用 Python 写脚本后再用 automator 来运行

参考: http://www.conxz.net/blog/2013/10/25/sloppy-python-snippets-to-capture-command-output/
'''
__author__ = '__L1n__w@tch'

import subprocess
import tkinter
import requests
import tkinter.messagebox
from library_wifi import ping_success


class MenuTool:
    """
    工具栏的类
    """

    def __init__(self):
        self.main_window = tkinter.Tk()
        self.__initialize_root()

        # 设置个大标题
        # self.__initialize_title()

        # 设置个列表, 显示相应按钮
        self.set_buttons()

        self.main_window.mainloop()

    def __initialize_root(self):
        """
        初始化根窗口
        :return:
        """
        # 设置窗口大小
        self.main_window.geometry("240x240")

        self.main_window.title("个人工具箱")

        # 居中操作
        self.main_window.update()  # update window ,must do
        current_width = self.main_window.winfo_reqwidth()  # get current width
        current_height = self.main_window.winfo_height()  # get current height
        screen_width, screen_height = self.main_window.maxsize()  # get screen width and height
        configuration = '%dx%d+%d+%d' % (current_width, current_height,
                                         (screen_width - current_width) / 2, (screen_height - current_height) / 2)
        self.main_window.geometry(configuration)

    def __initialize_title(self):
        """
        设置个大标题
        :return:
        """
        label_frame = tkinter.LabelFrame(self.main_window)
        title = tkinter.Text(label_frame)
        title.insert(tkinter.END, "个人工具箱")
        title.grid()
        label_frame.grid()

    def set_buttons(self):
        """
        设置相应按钮
        :return:
        """
        label_frame = tkinter.LabelFrame(self.main_window)
        list_box = tkinter.Listbox(label_frame)

        change_hidden_status_button = tkinter.Button(list_box, text="更改隐藏文件显示状态",
                                                     command=lambda: change_hidden_status_tool(True))
        login_school_wifi_button = tkinter.Button(list_box, text="登录西电校园网", command=lambda: logging_school_wifi(True))
        open_aria2c_button = tkinter.Button(list_box, text="开启 aria2c", command=open_aria2c)

        change_hidden_status_button.grid()
        open_aria2c_button.grid()
        login_school_wifi_button.grid()

        list_box.grid()
        label_frame.pack()


def change_hidden_status_tool(verbose=False):
    """
    改变隐藏文件显示状态, 如果运行前处于不显示则更改为显示, 如果为显示则更改为不显示
    :param verbose: 是否要开启弹窗提醒
    :return:
    """
    if verbose:
        tk = tkinter.Tk()
        tk.withdraw()

    cmd = "defaults read com.apple.finder AppleShowAllFiles -boolean"
    popen = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE)
    res = popen.stdout.readline().strip()

    change_command = "defaults write com.apple.finder AppleShowAllFiles -boolean {} ; killall Finder"
    if res == b"1":
        subprocess.call(change_command.format("false"), shell=True)
        tkinter.messagebox.showinfo("取消显示隐藏文件", "取消显示成功") if verbose else None
    elif res == b"0":
        subprocess.call(change_command.format("true"), shell=True)
        tkinter.messagebox.showinfo("显示隐藏文件", "显示隐藏文件成功") if verbose else None
    else:
        tkinter.messagebox.showerror("Something wrong!") if verbose else None

    exit()


def logging_school_wifi(verbose=False):
    """
    尝试登陆学校 wifi
    :return:
    """
    ifconfig_output = subprocess.check_output("ifconfig").decode()
    if "std-wlan" not in ifconfig_output.lower():
        tkinter.messagebox.showinfo("登录校园网", "你没连上学校 wifi 啊")
    else:
        # 认证页面
        url = "http://10.255.44.33:803/include/auth_action.php"
        post_data = {"action": "login", "username": "13030110024", "password": "foreachlf",
                     "ac_id": "1", "save_me": 0}  # &user_ip=&nas_ip=&user_mac=&save_me=0&ajax=1"}
        response = requests.post(url, post_data)

        if ping_success():
            tkinter.messagebox.showinfo("登录校园网", "登录成功") if verbose else None
        else:
            tkinter.messagebox.showerror("登录校园网", response.text) if verbose else None


def open_aria2c(verbose=False):
    """
    开启 aria2c 程序
    :param verbose: 是否显示详细信息
    :return:
    """
    subprocess.call("aria2c", shell=True)


if __name__ == "__main__":
    my_menu_tool = MenuTool()
