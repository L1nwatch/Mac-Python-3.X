#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
自己的 ui 的 main 脚本
"""

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from learning_pyqt.pyqt_from_ui import *

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    app = 0
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
