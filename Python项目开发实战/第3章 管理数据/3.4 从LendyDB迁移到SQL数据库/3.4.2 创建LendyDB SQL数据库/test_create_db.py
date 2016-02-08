#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 这部分书里没写,我自己测试出来的代码
'''
__author__ = '__L1n__w@tch'

import sqlite3
import re


def main():
    db = sqlite3.connect("test.db")
    cur = db.cursor()
    with open("lendydb.sql", "r") as f:
        scripts = f.read()

    # sql文件中存在几句drop语句,我把它删掉
    scripts = re.sub(r"drop[\s\S]*member;", "", scripts)
    print(scripts)
    cur.executescript(scripts)
    cur.close()
    db.close()


if __name__ == "__main__":
    main()
