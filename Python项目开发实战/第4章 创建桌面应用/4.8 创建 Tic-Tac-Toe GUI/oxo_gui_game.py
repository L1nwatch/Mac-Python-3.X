#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' oxo游戏的GUI界面的game模块
'''
__author__ = '__L1n__w@tch'

import tkinter.messagebox as mb
import oxo_logic

game_over = False


def ev_click(row, col):
    global game_over
    if game_over:
        mb.showerror("Game over", "Game over!")
        return
    game = cells2game()
    index = (3 * row) + col
    result = oxo_logic.user_move(game, index)
    game2cells(game)

    if not result:
        result = oxo_logic.computer_move(game)
        game2cells(game)
    if result == "D":
        mb.showinfo("Result", "It's a Draw!")
        game_over = True
    else:
        if result == "X" or result == "O":
            mb.showinfo("Result", "The winner is: {}".format(result))
            game_over = True


def game2cells(game):
    table = board.pack_slaves()[0]
    for row in range(3):
        for col in range(3):
            table.grid_slaves(row=row, column=col)[0]["text"] = game[3 * row + col]


def cells2game():
    values = []
    table = board.pack_slaves()[0]
    for row in range(3):
        for col in range(3):
            values.append(table.grid_slaves(row=row, column=col)[0]["text"])
    return values


def main():
    pass


if __name__ == "__main__":
    main()
