#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
尝试自己手动编写 pyqt5 例子
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    app = 0  # 加了这句之后就啥事都没有了, 神奇!!
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Hello PyQt')
    w.show()
    sys.exit(app.exec())
