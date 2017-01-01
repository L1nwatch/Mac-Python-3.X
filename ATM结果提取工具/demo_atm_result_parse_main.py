#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.21 调用 QT 创建的 UI
"""
import sys
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QErrorMessage)
from demo_atm_result_parse_tool import Ui_MainWindow  # 自己生成的 ui_py
from atm_result_collect import recursion_get_rate, get_json_data_from_result_url

__author__ = '__L1n__w@tch'


class MainWindow(Ui_MainWindow, QMainWindow):
    _window_list = []

    def __init__(self):
        super(MainWindow, self).__init__()

        MainWindow._window_list.append(self)

        self.setupUi(self)

        self.json_result = None  # 用来保留获取过的结果数据, 避免每次都得重新获取

    def add_layer(self):
        """
        获取用户输入的层次
        :return: int(), 层次
        """
        now_layer = self._get_layer()

        if now_layer is not None:
            # 在界面上增加层次
            next_layer = now_layer + 1
            self.lineEdit_2.setText(str(next_layer))

            # 显示结果
            self._show_layer_result_from_json_result()

    def _get_layer(self):
        """
        获取用户输入的层次
        :return: int(), 层次
        """
        try:
            now_layer = int(self.lineEdit_2.text())
            return now_layer
        except ValueError as e:
            self._show_error_message("层次输入有误: {}".format(str(e)))
            return False

    def sub_layer(self):
        """
        对应界面上的<减少层次>按钮
        :return:
        """
        now_layer = self._get_layer()

        if now_layer:
            # 在界面上减少层次
            next_layer = now_layer - 1
            self.lineEdit_2.setText(str(next_layer))

            # 显示结果
            self._show_layer_result_from_json_result()

    def _get_valid_url(self):
        """
        判断是否为合法的 URL, 合法格式如: http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec/results/585f344dd10540715b07f011
        :return: str(), 合法的 URL, 不合法则抛出 ValueError 异常
        """
        try:
            input_url = self.lineEdit.text()
            regex_format = "http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/atm/projects/[a-fA-F0-9]{24}/results/[a-fA-F0-9]{24}"
            return re.findall(regex_format, input_url, flags=re.IGNORECASE)[0]
        except:
            raise ValueError("URL 不合法")

    @staticmethod
    def _show_error_message(message):
        """
        弹出错误消息框
        :param message: 消息内容
        :return: None
        """
        error_message_window = QErrorMessage()
        error_message_window.setWindowTitle("发现错误")
        error_message_window.showMessage(message)
        error_message_window.exec_()

    def _show_layer_result_from_json_result(self):
        """
        显示 json 结果到窗口中
        :return: None
        """
        layer = int(self.lineEdit_2.text())

        layer_result = recursion_get_rate(self.json_result, layer)
        self.plainTextEdit.setPlainText("\n".join(layer_result))

    def get_result(self):
        try:
            # 获取输入的 URL 及 层次
            result_url = self._get_valid_url()

            self.json_result = get_json_data_from_result_url(result_url)
            self._show_layer_result_from_json_result()
        except ValueError as e:
            self._show_error_message("输入有误: {}".format(str(e)))
        except Exception as e:
            self._show_error_message("未知错误: {}".format(str(e)))


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(a.exec_())
