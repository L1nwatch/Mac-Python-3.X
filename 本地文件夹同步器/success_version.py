#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 本程序的目的, 拷贝所有老师放在桌面上的学习资料

实现: 当教室电脑刚开机时, 进行检查, 如果文件已经复制, 就删除掉; 否则进行复制操作
当教室电脑待机时, 每隔 60s 检查桌面是否有新文件复制进来, 如果有, 则进行复制操作; 否则什么都不做

本程序从 configure.json 中读取配置
'''
# TODO 当retention文件被删除时,不提供恢复功能
__author__ = '__L1n__w@tch'

import time
import os
import shutil
import filecmp
import json
import distutils.dir_util


class FilesSaver:
    def __init__(self, configure_name="configure.json"):
        configure = self.read_configure(configure_name)
        self.source_path = configure["source"]
        self.destination_path = configure["destination"]
        self.retain_files = set(configure["retention"])
        self.closure = bool(configure["closure"])

    def _ensure_dir_exists(self):
        if not os.path.exists(self.destination_path):
            os.mkdir(self.destination_path)

    def _check(self, file_name):
        """
        检查目标文件夹, 看是否需要复制path指向的文件, 需要则返回True
        :param file_name: "file.txt"
        :return: True or False
        """
        # 检查是否已经复制
        if file_name not in os.listdir(self.destination_path):
            return True

        # 已复制, 则检查是否相同
        path1 = os.path.join(self.source_path, file_name)
        path2 = os.path.join(self.destination_path, file_name)
        if os.path.isdir(path1):
            result = filecmp.dircmp(path1, path2)
            if self.closure is True:  # 配置开启递归检查目录, 否则只检查当前目录
                return self._check_dir_closure(result) is True
            else:
                return len(result.left_only) > 0 or len(result.diff_files) > 0
        else:
            return filecmp.cmp(path1, path2) is False

    # 递归的检查目录, 如果存在不同则返回True, 否则返回None
    def _check_dir_closure(self, dir_cmp):
        if len(dir_cmp.left_only) > 0:
            return True
        for sd in dir_cmp.subdirs.values():
            return self._check_dir_closure(sd)

    def ensure(self):
        """
        确保源文件夹中除了保留文件列表以外的文件都拷贝进了目标文件夹
        :return: None
        """
        self._ensure_dir_exists()
        wait_to_check = set(os.listdir(self.source_path)) - self.retain_files
        for file_name in wait_to_check:
            if self._check(file_name):
                path = os.path.join(self.source_path, file_name)
                if os.path.isdir(path):
                    distutils.dir_util.copy_tree(path, os.path.join(self.destination_path, file_name))
                else:
                    shutil.copy(path, self.destination_path)

    def delete(self):
        """
        删除源文件夹中除了保留文件列表以外的文件
        :return: None
        """
        for file in os.listdir(self.source_path):
            if file not in self.retain_files:
                path = os.path.join(self.source_path, file)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)

    def read_configure(self, name):
        with open(name) as f:
            json_data = f.read()
            return json.loads(json_data)


def main():
    files_saver = FilesSaver()

    # 教室电脑刚开机
    files_saver.ensure()
    files_saver.delete()

    # 教室电脑待机中
    while True:
        time.sleep(60)
        files_saver.ensure()


if __name__ == "__main__":
    main()
