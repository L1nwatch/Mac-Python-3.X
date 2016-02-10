#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 基于tkinter重新实现了tic-tac-toe游戏的图形化界面,把tkinter几个模块的代码都整合在了一起
'''
__author__ = '__L1n__w@tch'

import tkinter as tk
import tkinter.messagebox as mb
import oxo_logic

top = board = status = None


def build_menu(parent):
    """
    菜单结构被定义为一组嵌套元组.叶节点菜单项包含了名称-函数对.
    然后创建顶层菜单栏对象并循环数据结构,创建了子菜单并将它们插入到菜单栏中,最后返回完整的菜单栏对象
    :param parent:
    :return:
    """
    global ev_new, ev_resume, ev_save, ev_exit, ev_help, ev_about
    menus = (("File", (("New", ev_new), ("Resume", ev_resume), ("Save", ev_save), ("Exit", ev_exit))),
             ("Help", (("Help", ev_help), ("About", ev_about))))
    menu_bar = tk.Menu(parent)
    for menu in menus:
        m = tk.Menu(parent)
        for item in menu[1]:
            m.add_command(label=item[0], command=item[1])
        menu_bar.add_cascade(label=menu[0], menu=m)

    return menu_bar


def build_board(parent):
    outer = tk.Frame(parent, border=2, relief="sunken")
    inner = tk.Frame(outer)
    inner.pack()

    # 使用网格布局管理器而不是封装器,因为面板布局完美地匹配网格布局风格
    for row in range(3):
        for col in range(3):
            cell = tk.Button(inner, text=" ", width="5", height="2", command=lambda r=row, c=col: ev_click(r, c))
            cell.grid(row=row, column=col)
    return outer


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


def ev_new():
    global status
    status["text"] = "Playing game"
    game2cells(oxo_logic.new_game())


def ev_resume():
    global status
    status["text"] = "Playing game"
    game = oxo_logic.restore_game()
    game2cells(game)


def ev_save():
    game = cells2game()
    oxo_logic.save_game(game)


def ev_exit():
    global status
    if status["text"] == "Playing game":
        if mb.askyesno("Quitting", "Do you want to save the game before quitting?"):
            ev_save()
    top.quit()


def ev_help():
    mb.showinfo("Help", """
    File    ->  New: starts a new game of tic-tac-toe
    File    ->  Resume: restores the last saved game and commences play
    File    ->  Save: Saves current game
    File    ->  Exit: quits, prompts to save active game
    Help    ->  Help: shows this page
    Help    ->  About: Shows information about the program and author""")


def ev_about():
    mb.showinfo("About", "Tic - tac - toe game GUI demo by Alan Gauld(Copy by {})".format(__author__))


def ev_click(row, col):
    global status
    if status["text"] == "Game Over":
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
        status["text"] = "Game Over"
    elif result == "X" or result == "O":
        mb.showinfo("Result", "The winner is: {}".format(result))
        status["text"] = "Game Over"


def main():
    global top, board, status
    top = tk.Tk()
    m_bar = build_menu(top)
    top["menu"] = m_bar

    board = build_board(top)
    board.pack()
    status = tk.Label(top, text="Playing game", border=0, background="lightgrey", foreground="red")
    status.pack(anchor="s", fill="x", expand=True)

    tk.mainloop()


if __name__ == "__main__":
    main()
