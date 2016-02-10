#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' argparse模块示例代码
'''
__author__ = '__L1n__w@tch'

import argparse as ap
import oxo_ui


def main():
    p = ap.ArgumentParser(description="Play a game of Tic - Tac - Toe")
    # 创建一些作为互相独立的组的选项
    grp = p.add_mutually_exclusive_group()
    # 通过指定action的值为store_true,将选项变成了布尔值
    grp.add_argument("-n", "--new", action="store_true", help="start new game")
    grp.add_argument("-r", "--res", "--restore", action="store_true", help="restore old game")

    args = p.parse_args()
    if args.new:
        oxo_ui.execute_choice(1)
    elif args.res:
        oxo_ui.execute_choice(2)
    else:
        while True:
            choice = oxo_ui.get_menu_choice(oxo_ui.menu)
            oxo_ui.execute_choice(choice)


if __name__ == "__main__":
    main()
