#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
功能测试, 对自己的集成工具箱进行功能测试
"""
import unittest
import subprocess
import os
import random
import string
from menu_tool import change_hidden_status_tool

__author__ = '__L1n__w@tch'


class TestShowHiddenTools(unittest.TestCase):
    """
    对显示隐藏文件的那个工具进行功能测试
    """

    def setUp(self):
        """
        测试前的初始化操作
        :return:
        """
        # 创建一个隐藏文件用于测试
        self.hidden_file = "".join([random.choice(string.ascii_letters) for i in range(random.randint(1, 23))])
        self.create_a_hidden_file(self.hidden_file)

        # 设置隐藏的命令
        self.hide_cmd = "defaults write com.apple.finder AppleShowAllFiles -boolean {} ; killall Finder"

        # 获取目前系统是隐藏文件还是可以显示隐藏文件
        self.status = self.check_system_file_hide_status()

    def tearDown(self):
        """
        回复测试前的初始状态
        :return:
        """
        # 删除文件
        os.remove(self.hidden_file)

        # 设置回测试前的状态
        if self.status != self.check_system_file_hide_status():
            if self.status == "不显示隐藏文件":
                subprocess.call(self.hide_cmd.format("false"), shell=True)
            else:
                subprocess.call(self.hide_cmd.format("true"), shell=True)

    @classmethod
    def create_a_hidden_file(cls, file_name):
        """
        创建一个隐藏文件
        :param file_name: 文件名
        :return:
        """
        with open(file_name, "w") as  f:
            f.write("aaa")

        subprocess.call("chflags hidden {}".format(file_name), shell=True)

    @classmethod
    def check_system_file_hide_status(cls):
        """
        检查目前系统是处于隐藏文件状态还是显示隐藏文件状态
        :return: "显示隐藏文件" or "不显示隐藏文件"
        """
        status = {b"1": "显示隐藏文件", b"0": "不显示隐藏文件"}

        cmd = "defaults read com.apple.finder AppleShowAllFiles -boolean"
        popen = subprocess.Popen(cmd, shell=True,
                                 stdout=subprocess.PIPE)
        res = popen.stdout.readline().strip()

        return status[res]

    def test_hide_files(self):
        """
        测试能否隐藏文件
        :return:
        """
        # 设置处于显示模式
        subprocess.call(self.hide_cmd.format("true"), shell=True)

        # 运行显示隐藏文件的工具
        change_hidden_status_tool()

        # 检查是否隐藏了
        self.assertEqual(self.check_system_file_hide_status(), "不显示隐藏文件")

    def test_show_hidden_files(self):
        """
        测试能否显示隐藏文件
        :return:
        """
        # 设置处于隐藏模式
        subprocess.call(self.hide_cmd.format("false"), shell=True)

        # 运行显示隐藏文件的工具
        change_hidden_status_tool()

        # 检查是否显示了出来
        self.assertEqual(self.check_system_file_hide_status(), "显示隐藏文件")


if __name__ == "__main__":
    unittest.main()
