#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 自从用了 Mac 后, 每次来到图书馆都得重新登录一下才能使用校园网, 所以干脆些了个程序来完成登录工作
'''
__author__ = '__L1n__w@tch'

import requests
import tkinter.messagebox


def main():
    url = "http://10.255.44.33/cgi-bin/do_login"
    post_data = {"action": "login", "username": "13030110024", "password": "bedd129c3adfa9fa", "type": "1"}
    response = requests.post(url, post_data)
    tkinter.messagebox.showinfo(title="登录校园网", message=response.text)


if __name__ == "__main__":
    main()
