#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.11.26 每一个案例爬一次太慢了, 这里也得优化成只爬一次
2016.11.20 分为功能测试和单元测试文件, 这是功能测试文件
2016.11.16 作为爬虫的测试文件
"""
import unittest
import os
from atm_scrapy import ATMScrapy
from my_constant import const

__author__ = '__L1n__w@tch'


class FunctionalTestATMScrapy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_project_id = "53c49025d105401f5e0003ec"
        cls.test_path = os.path.join(os.curdir, "test_for_functional")
        cls.test_atm_crawl = ATMScrapy(project_url=cls.test_project_id)

        # Y 运行了这个工具
        cls.test_atm_crawl.crawl()

    def test_can_get_all_dir_name(self):
        """
        测试能够获取目录树下的所有文件夹名, 要测试一级目录一直到五级目录
        :return:
        """
        # Y 想检查一下工具是否下载全了, 于是随便找了个目录来对照, 看是否跟 ATM 页面上的目录相一致
        test_dir = self.test_path
        for next_dir in ["预发布项自动化案例", "发布测试项案例新增", "lf", "14-系统维护", "系统更新"]:
            test_dir = os.path.join(test_dir, next_dir)
            self.assertTrue(os.path.exists(test_dir))

    def test_can_parse_dir_tree(self):
        """
        测试能够正确解析目录树, 即按照目录树的层次结构创建对应的文件夹并摆放文件
        :return:
        """
        # Y 想看一下下载到的几个父级文件夹是否跟 ATM 页面上的一致
        page_parent_dirs = ["必选发布测试项new", "储运母盘测试(适用于32G SSD)", "回收站", "AF7.2自动化", "AF7.0", "调试测试套",
                            "定制-snj", "AF7.1R1发布测试项", "预发布项自动化案例", "AF7.1R1母盘验证", "AF7.1R2 utm 改进"]
        self.assertTrue(all(os.path.exists(os.path.join(self.test_path, next_dir)) for next_dir in page_parent_dirs))

    def test_can_get_all_content(self):
        """
        测试下载下来的是一个案例里面所有的内容, 而不只是一部分
        :return:
        """
        # Y 打开了其中一个案例, 想看看跟 ATM 平台上的是否一致
        file_path = os.path.join(self.test_path, "必选发布测试项new", "发布测试项", "前置", "新需求-区域-勾我")
        with open(file_path, "r") as f:
            data = f.read()

        with open("right_content_for_test.txt", "r") as f:
            right_content = f.read()
        self.assertEqual(data, right_content)

    @unittest.skipIf(True, "一开始写的测试,现在方法变了,需要评估")
    def test_can_parse_url_right(self):
        """
        测试给定一个参数, 如果给了不同形式的, 比如加上 http 前缀, 都能够正确获取到自己要的 id 信息
        :return:
        """
        # Y 故意输入一个错误的 url
        response = self.test_atm_crawl.crawl(self.test_project_id + "12321321", os.curdir)

        # Y 得到了一个错误的提示
        self.assertEqual(response, "invalid project id!")

        # Y 输入的不止是一个 url, 而且还故意不输入存放路径
        response = self.test_atm_crawl.crawl("http://200.200.0.33/atm/projects/{}".format(self.test_project_id))

        # Y 发现还是成功更新了
        self.assertTrue(const.SUCCESS_MESSAGE in response)

    @unittest.skipIf(True, "还没实现")
    def test_crawl_once_in_limit_time(self):
        """
        测试爬虫在一定时间内不会重复爬
        :return:
        """
        # Y 运行了这个工具
        response = self.test_atm_crawl.crawl(self.test_project_id, os.curdir)

        # Y 看到提示说是下载成功了
        self.assertEqual(const.SUCCESS_MESSAGE in response)

        # Y 紧接着再次运行这个工具
        response = self.test_atm_crawl.crawl(self.test_project_id)

        # Y 看到提示说是短时间内不能连续运行 2 次
        self.assertEqual(const.CONTINUE_RUN_TIME_LIMIT, response)


if __name__ == "__main__":
    pass
