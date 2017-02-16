#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.16 开始创建图形界面的文件内容搜索器
"""
import os
import sys
import threading
from search_tool_main_window import Ui_MainWindow  # 自己生成的 ui_py
from search_keyword import is_valid_file_type, search_keyword_infile

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QErrorMessage, QTableWidgetItem

__author__ = '__L1n__w@tch'


class MainWindow(Ui_MainWindow, QMainWindow):
    _window_list = []

    def __init__(self):
        super(MainWindow, self).__init__()

        MainWindow._window_list.append(self)

        self.setupUi(self)

        self.result_table.horizontalHeader().setStretchLastSection(True)

    def input_search_path(self):
        """
        实现读取搜索路径, 然后设置到对应的窗格中
        """
        root_dir = QFileDialog.getExistingDirectory(self, "请选择文件夹路径")
        self.root_path_edit.setText(root_dir)

    def show_error_message(self, error_message):
        """
        负责弹出错误消息框
        :param error_message: 消息框里面的内容
        :return: None
        """
        error = QErrorMessage()
        error.showMessage(error_message)
        error.exec_()

    def initialize(self):
        path = self.root_path_edit.text()
        if path == "":
            raise RuntimeError("没有设定搜索路径")

        file_type = self.file_type_edit.text()
        if file_type == "":
            raise RuntimeError("没有输入要搜索的文件类型")
        try:
            file_type = self.get_file_type(file_type)
        except ValueError:
            raise RuntimeError("要搜索的关键词不合法")

        ignore_case = self.ignore_case_box.isChecked()

        keyword = self.keyword_edit.text()
        if keyword == "":
            raise RuntimeError("没有输入要搜索的关键词")

        return path, file_type, ignore_case, keyword

    @staticmethod
    def get_file_type(raw_str):
        return raw_str.split("#")

    def begin_search(self, root_path, file_type, ignore_case, keyword):
        counts = 0
        for root, dirs, files in os.walk(root_path):
            for each_file in files:
                if is_valid_file_type(each_file, file_type):
                    path = root + os.sep + each_file
                    line_content = search_keyword_infile(path, keyword, ignore_case)
                    if line_content:
                        self.result_table.insertRow(counts)

                        content_path = QTableWidgetItem(".{}".format(path[len(root_path):]))
                        self.result_table.setItem(counts, 0, content_path)

                        content = QTableWidgetItem(line_content.strip())
                        self.result_table.setItem(counts, 1, content)

                        counts += 1
                        self.result_table.setRowCount(counts)

        self.state_label.setText("搜索结束")

    def run(self):
        """
        开始搜索
        :return:
        """
        try:
            # 初始化各项参数, 确保均有值
            path, file_type, ignore_case, keyword = self.initialize()

            # 开始递归搜索
            self.state_label.setText("搜索 ing")
            search_thread = threading.Thread(target=self.begin_search, args=(path, file_type, ignore_case, keyword))
            search_thread.start()

        except RuntimeError as e:
            self.show_error_message(str(e))


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(a.exec_())
