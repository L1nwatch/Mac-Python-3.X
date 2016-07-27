#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
对自己编写的功能测试和程序进行功能测试
"""
import unittest
import os
import subprocess
import random
import string
from functional_tests import TestShowHiddenTools

__author__ = '__L1n__w@tch'


class TestFunctionalTest(unittest.TestCase):
    """
    对自己的功能测试进行测试
    """

    def setUp(self):
        """
        初始化
        :return:
        """
        self.file_name = "".join([random.choice(string.ascii_letters) for i in range(random.randint(1, 23))])

    def tearDown(self):
        """
        还原初始化
        :return:
        """
        # 删除该文件
        os.remove(self.file_name)

    def test_create_a_hidden_file(self):
        """
        测试是否成功创建了一个文件
        :return:
        """
        # 检查原先是否没有该文件
        if os.path.exists(self.file_name):
            self.assertFalse("已经存在测试文件, 求换一个文件名")

        tools = TestShowHiddenTools()
        tools.create_a_hidden_file(self.file_name)

        # 检查是否有了该文件
        self.failIf(not os.path.exists(self.file_name), "创建文件失败")

        # 检查是否为隐藏文件
        output = subprocess.check_output(["ls", "-al"]).decode().split("\n")
        for each_file in output:
            if self.file_name in each_file:
                self.assertIn("@", each_file, "不是隐藏文件")




if __name__ == "__main__":
    pass
