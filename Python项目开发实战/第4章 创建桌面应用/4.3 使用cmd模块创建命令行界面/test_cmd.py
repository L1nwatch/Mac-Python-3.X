#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 基于cmd模块构建 tic-tac-toe 游戏的骨架
'''
__author__ = '__L1n__w@tch'

import cmd, oxo_ui, oxo_logic


class Oxo_cmd(cmd.Cmd):
    intro = "Enter a command: new, resume, quit. Type 'help' or '?' for help"
    prompt = "(oxo) "
    game = ""

    # 定义一组以do_开头的方法.这个类将下划线后面的部分解释为用户可以输入的命令
    # 注意,不需要一个帮助命令,因为它已经被自动创建在类机制中了.注意还需要在方法定义中提供第二个虚拟参数,即使在方法中没有使用它
    def do_new(self, arg):
        self.game = oxo_logic.new_game()
        oxo_ui.play_game(self.game)

    def do_resume(self, arg):
        self.game = oxo_logic.restore_game()
        oxo_ui.play_game(self.game)

    def do_quit(self, arg):
        print("Goodbye...")
        raise SystemExit


def main():
    game = Oxo_cmd().cmdloop()


if __name__ == "__main__":
    main()
