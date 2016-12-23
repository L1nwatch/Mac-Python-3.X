#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.21 调用 QT 创建的 UI
"""
__author__ = '__L1n__w@tch'

import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    if app.exec_():
        sys.ext()
