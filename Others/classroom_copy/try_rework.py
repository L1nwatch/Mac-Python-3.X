#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 本程序的目的, 拷贝所有老师放在桌面上的学习资料

实现: 当教室电脑刚开机时, 进行检查, 如果文件已经复制, 就删除掉; 否则进行复制操作
当教室电脑待机时, 每隔 60s 检查桌面是否有新文件复制进来, 如果有, 则进行复制操作; 否则什么都不做

本程序从 goodgoodstudy.ini 中读取配置
'''
__author__ = '__L1n__w@tch'

import time
import os
import shutil
import filecmp

source = r"C:\Users\Administrator.hp-PC\Desktop"
destination = r"E:\goodgoodstudy"
retention_files = {"Software", "网安Subjects", "MathType"}


class FilesSaver:
    def __init__(self, source_path, destination_path, retain_files=set()):
        self.source_path = source_path
        self.destination_path = destination_path
        self.retain_files = retain_files

    def _ensure_dir_exists(self):
        if not os.path.exists(self.destination_path):
            os.mkdir(self.destination_path)

    def _needs_to_copy(self):
        pass

    def _check(self, path):
        # 检查是否已经复制
        for each_path in os.listdir(self.destination_path):
            if path not in each_path:
                return True

        # 已复制, 则检查是否相同
        if found:
            pass


    def ensure(self):
        """
        确保源文件夹中除了保留文件列表以外的文件都拷贝进了目标文件夹
        :return: None
        """
        self._ensure_dir_exists()
        wait_to_check = set(os.listdir(self.source_path)) - self.retain_files
        for each_path in wait_to_check:
            if self._check(each_path):
                if os.path.isdir(each_path):
                    shutil.copytree(each_path, self.destination_path)
                else:
                    shutil.copy(each_path, self.destination_path)

    def delete(self):
        """
        删除源文件夹中除了保留文件列表以外的文件
        :return: None
        """
        for file in os.listdir(self.source_path):
            if file not in self.retain_files:
                if os.path.isdir(file):
                    shutil.rmtree(file)
                else:
                    os.remove(file)


def main():
    files_saver = FilesSaver(source, destination, retention_files)

    # 教室电脑刚开机
    files_saver.ensure()
    files_saver.delete()

    # 教室电脑待机中
    while True:
        time.sleep(60)
        files_saver.ensure()


if __name__ == "__main__":
    main()
