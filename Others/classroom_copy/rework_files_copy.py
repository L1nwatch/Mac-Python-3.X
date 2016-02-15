#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
'''
需求：
1. 每次开机检查一次桌面, 把新文件都拷贝一遍然后删除
2. 每隔60s检查一次桌面, 拷贝新文件
'''
__author__ = '__L1n__w@tch'

import time
import os
import shutil


# shutil库：http://www.cnblogs.com/vamei/archive/2012/09/14/2684775.html
# shutil库用来文件管理的
# xcopy: http://wenku.baidu.com/link?url=-wW16GZupboypX36MCnduNIulA64D_WiVJG7nFSFO6giIf4Ta_yC4Y55JLtKvPIAyE1LYXDZ2acoDbi62GKE-ygEqD0TgooWwrRXczKHGci

def main():
    # 先执行一次检查桌面（开机时运行这个）
    desktop_path = r"C:\Users\Administrator.hp-PC\Desktop"
    target_path = r"E:\goodgoodstudy"
    file_set = {"Software", "网安Subjects", "MathType"}

    checker = DesktopChecker(desktop_path, target_path, file_set)
    checker.check(first_check=True)
    checker.delete()

    # 每隔60s检查一次桌面
    while True:
        time.sleep(60)
        checker.check()


class DesktopChecker:
    def __init__(self, desktop_path, target_path, file_set):
        self.desktop_path = desktop_path
        self.target_path = target_path
        self.file_set = set(file_set)
        if not os.path.exists(self.target_path):
            os.mkdir(self.target_path)

    def check(self, first_check=False):
        file_set = set(os.listdir(self.desktop_path))
        new_file_set = file_set - self.file_set
        if len(new_file_set) > 0:
            for each_file in new_file_set:
                if first_check == True or self.need_copys(each_file):
                    self.copy_file(each_file)

    def copy_file(self, file_name):
        source = os.path.join(self.desktop_path, file_name)
        destination = os.path.join(self.target_path, file_name)
        try:
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copyfile(source, destination)
        except:
            os.system("xcopy {0} {1} /S/Y".format(source, destination))

    def need_copys(self, file_name):
        exist_file_set = set(os.listdir(self.target_path))
        if file_name in exist_file_set:
            if not self.is_new(file_name):
                return False
        return True

    def is_new(self, file_name):
        new_file_mtime = os.path.getmtime(os.path.join(self.desktop_path, file_name))
        old_file_mtime = os.path.getmtime(os.path.join(self.target_path, file_name))
        return new_file_mtime > old_file_mtime

    def delete(self):
        file_set = set(os.listdir(self.desktop_path))
        new_file_set = file_set - self.file_set
        for each_file in new_file_set:
            path = self.desktop_path + os.sep + each_file
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)


if __name__ == "__main__":
    main()
