#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' oxo_data is the data module for a tic - tac - toe (or OXO) game.
It saves and restores a game board. The functions are:
    save_game(game) ->  None
    restore_game()  ->  game
Note that no limits are placed on the size of data.
The game implementation is responsible for validating all data in and out.
'''
__author__ = '__L1n__w@tch'

import os.path

game_file = ".oxogame.dat"


# 按照惯例,不希望被模块使用者调用的函数会在名字前加一个下划线
def _get_path():
    """
    Returns a valid path for data file.
    Tries to use the users home folder, defaults to cwd
    :return: string
    """
    # 使用os模块试图得到用户的主目录,如果失败就使用当前目录
    try:
        game_path = os.environ["HOMEPATH"] or os.environ["HOME"]
        if not os.path.exists(game_path):
            game_path = os.getcwd()
    except (KeyError, TypeError):
        game_path = os.getcwd()
    return game_path


def save_game(game):
    """
    saves a game object in the data file in the users home folder.
    No checking is done on the input, which is expected to be a list of characters
    :param game:
    :return: None
    """
    path = os.path.join(_get_path(), game_file)
    with open(path, "w") as gf:
        game_str = "".join(game)
        gf.write(game_str)


def restore_game():
    """
    Restores a game from the data file.
    The game object is a list of characters
    :return: game
    """
    path = os.path.join(_get_path(), game_file)
    with open(path) as gf:
        game_str = gf.read()
        return list(game_str)


def test():
    print("Path = ", _get_path())
    save_game(list("XO XO OX"))
    print(restore_game())


def main():
    test()


if __name__ == "__main__":
    main()
