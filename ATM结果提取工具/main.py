#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.21 调用 QT 创建的 UI
"""
__author__ = '__L1n__w@tch'

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from demo_atm_result_parse_tool import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    pass


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(a.exec_())
