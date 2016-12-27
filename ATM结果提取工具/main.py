#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.21 调用 QT 创建的 UI
"""
__author__ = '__L1n__w@tch'

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import demo_atm_result_parse_tool

if __name__ == '__main__':
    app = 0
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = demo_atm_result_parse_tool.Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
