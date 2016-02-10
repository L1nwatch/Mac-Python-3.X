#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' This is the main logic for a tic - tac - toe game.
It is not optimised for a quality game it simply generates random moves and checks the results of a move for a winning line.
Exposed functions are:
    new_game()
    save_game()
    restore_game()
    user_move()
    computer_move()
'''
__author__ = '__L1n__w@tch'

import os, random
import oxo_data


def new_game():
    return list(" " * 9)


def save_game(game):
    oxo_data.save_game(game)


def restore_game():
    """
    捕捉任何由于找不到数据文件所抛出的错误并验证保存游戏的长度
    :return:
    """
    try:
        game = oxo_data.restore_game()
        if len(game) == 9:
            return game
        else:
            return new_game()
    except IOError:
        return new_game()


def _generate_move(game):
    """
    寻找当前游戏中没有被使用的格子,并随机选择一个作为计算机的移动
    :param game:
    :return:
    """
    options = [i for i in range(len(game)) if game[i] == " "]
    return random.choice(options)


def _is_winning_move(game):
    """
    只有8个可能的获胜路线.
    :param game:
    :return:
    """
    wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

    for a, b, c in wins:
        chars = game[a] + game[b] + game[c]
        if chars == "XXX" or chars == "OOO":
            return True
    return False


def user_move(game, cell):
    """
    一个空字符串意味着游戏仍然继续,X或O意味着获胜,而D意味着平局
    :param game:
    :param cell:
    :return:
    """
    if game[cell] != " ":
        raise ValueError("Invalid cell")
    else:
        game[cell] = "X"
    if _is_winning_move(game):
        return "X"
    else:
        return ""


def computer_move(game):
    cell = _generate_move(game)
    if cell == -1:
        return "D"
    game[cell] = "O"
    if _is_winning_move(game):
        return "O"
    else:
        return ""


def test():
    result = ""
    game = new_game()
    while not result:
        print(game)
        try:
            result = user_move(game, _generate_move(game))
        except ValueError:
            print("Oops, that shouldn't happen")
        if not result:
            result = computer_move(game)

        if not result:
            continue
        elif result == "D":
            print("Its a draw")
        else:
            print("Winner is:", result)
        print(game)


def main():
    test()


if __name__ == "__main__":
    main()
