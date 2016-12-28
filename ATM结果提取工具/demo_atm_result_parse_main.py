#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.21 调用 QT 创建的 UI
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from demo_atm_result_parse_tool import Ui_MainWindow    # 自己生成的 ui_py

__author__ = '__L1n__w@tch'


class MainWindow(Ui_MainWindow, QMainWindow):
    _window_list = []

    def __init__(self):
        super(MainWindow, self).__init__()

        MainWindow._window_list.append(self)

        self.setupUi(self)

    def add_layer(self):
        pass

    def sub_layer(self):
        pass

    def get_result(self):
        pass

if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(a.exec_())
