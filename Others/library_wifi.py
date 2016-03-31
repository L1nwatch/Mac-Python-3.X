#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 自从用了 Mac 后, 每次来到图书馆都得重新登录一下才能使用校园网, 所以干脆些了个程序来完成登录工作
'''
__author__ = '__L1n__w@tch'

import requests
import tkinter.messagebox
import tkinter
import subprocess


def old_login():
    """
    2016.03.10 还可以用的登录方式, 隔了一天就不能用了...
    :return:
    """
    url = "http://10.255.44.33/cgi-bin/do_login"
    post_data = {"action": "login", "username": "13030110024", "password": "bedd129c3adfa9fa", "type": "1"}
    response = requests.post(url, post_data)
    if "62208306347465" in response.text:
        tkinter.messagebox.showinfo(title="登录校园网", message="登录成功")
        return True
    else:
        # tkinter.messagebox.showerror(title="登录校园网", message="登录失败,未知错误: {}".format(response.text))
        return False


def new_login():
    """
    2016.03.10 测试
    :return:
    """
    url = "http://192.168.253.2/portal/pws?t=li"
    s = requests.Session()
    s.get(url)
    post_data = {"userName": "13030110024", "userPwd": "Zm9yZWFjaGxm"}
    response = s.post(url, post_data)
    if ping_success():
        tkinter.messagebox.showinfo(title="登录校园网", message="登录成功")
        return True
    else:
        # tkinter.messagebox.showinfo(title="登录校园网", message=response.text)
        return False


def lab_login():
    """
    在 F520 登录地点
    :return:
    """
    # &ac_id=6&type=1&wbaredirect=&mac=&user_ip=
    url = "http://10.255.44.33/cgi-bin/srun_portal"
    post_data = {"action": "login", "username": "13030110024", "password": "foreachlf", "ac_id": 6}
    s = requests.Session()
    response = s.get(url)
    response = s.post(url, post_data)
    if ping_success():
        tkinter.messagebox.showinfo(title="登录校园网", message="登录成功")
        return True
    else:
        tkinter.messagebox.showinfo(title="登录校园网", message=response.text)
        return False


def ping_success():
    res = subprocess.call("ping -c 2 www.baidu.com", shell=True)
    return res == 0


def main():
    tk = tkinter.Tk()
    tk.withdraw()  # 去掉空窗口

    tkinter.messagebox.showerror("啊啊啊啊啊", "自从认证系统更新后我还没有时间写这个程序")
    exit()

    if not old_login() and not new_login():
        lab_login()


if __name__ == "__main__":
    main()
