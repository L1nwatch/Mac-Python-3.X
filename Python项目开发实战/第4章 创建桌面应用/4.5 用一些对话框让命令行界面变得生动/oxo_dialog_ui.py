#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import tkinter
import tkinter.messagebox as mb
import oxo_logic

menu = ["Start new game", "Resume saved game", "Display help", "Quit"]


def get_menu_choice(a_menu):
    """
    takes a list of strings as input, displays as a numbered menu and loops until user selects a valid number
    :param a_menu: ["Start new game", "Resume saved game", "Display help", "Quit"]
    :return: int, 1 or 2 or 3 or 4
    """
    if not a_menu:
        raise ValueError("No menu content")
    while True:
        print("\n\n")
        for index, item in enumerate(a_menu):
            print(index + 1, "\t", item)
        try:
            choice = int(input("\nChoose a menu option: "))
            if 1 <= choice <= len(a_menu):
                return choice
            else:
                print("Choose a number between 1 and", len(a_menu))
        except ValueError:
            print("Choose the number of a menu option")


def start_game():
    return oxo_logic.new_game()


def resume_game():
    return oxo_logic.restore_game()


def display_help():
    print("""
    Start new game: starts a new game of tic - tac - toe
    Resume saved game: restores the last saved game and commences play
    Display help: shows this page
    Quit: quits the application
    """)


def quit_game():
    print("Goodbye...")
    raise SystemExit


def execute_choice(choice):
    """
    Execute whichever option the user selected. If the choice produces a valid game then play the game until it completes.
    :param choice: int
    :return: None
    """
    dispatch = [start_game, resume_game, display_help, quit_game]
    game = dispatch[choice - 1]()
    if game:
        play_game(game)


def print_game(game):
    display = """
    1 | 2 | 3   {} | {} | {}
    ---------   ------------
    4 | 5 | 6   {} | {} | {}
    ---------   ------------
    7 | 8 | 9   {} | {} | {}"""
    print(display.format(*game))


def play_game(game):
    result = ""
    while not result:
        print_game(game)
        choice = input("Cell[1-9 or q to quit]: ")
        if choice.lower()[0] == "q":
            save = mb.askyesno("Save game", "Save game before quitting?")
            if save:
                oxo_logic.save_game(game)
            quit_game()
        else:
            try:
                cell = int(choice) - 1
                if not (0 <= cell <= 8):  # check range
                    raise ValueError
            except ValueError:
                print("Choose a number between 1 and 9 or 'q' to quit ")
                continue

            try:
                result = oxo_logic.user_move(game, cell)
            except ValueError:
                mb.showerror("Invalid cell", "Choose an empty cell")
                continue
            if not result:
                result = oxo_logic.computer_move(game)
            if not result:
                continue
            elif result == "D":
                print_game(game)
                mb.showinfo("Result", "It's a draw")
            else:
                print_game(game)
                mb.showinfo("Result", "Winner is {}".format(result))


def main():
    top = tkinter.Tk()
    top.withdraw()
    while True:
        choice = get_menu_choice(menu)
        execute_choice(choice)


if __name__ == "__main__":
    main()
