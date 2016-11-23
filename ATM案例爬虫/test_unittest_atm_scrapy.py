#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.11.22 新增两个单元测试并且通过了, 分别是获取项目 id 以及下载 json 文件
2016.11.20 作为爬虫的测试文件, 这里存放的是单元测试文件
"""
import os
import unittest
import random
import string
from my_constant import const
from atm_scrapy import ATMScrapy

__author__ = '__L1n__w@tch'


class UnittestATMScrapy(unittest.TestCase):
    def setUp(self):
        self.test_atm_scrapy = ATMScrapy()
        self.test_project_id = "53c49025d105401f5e0003ec"

    def test_can_download_json_file_from_project_id(self):
        """
        测试给定一个项目id, 能够下载到 json 文件并命名为 id.json
        :return:
        """
        response = self.test_atm_scrapy.download_tree_json_file(
            "http://200.200.0.33/atm/projects/{}".format(self.test_project_id))
        self.assertTrue(response in const.SUCCESS_MESSAGE)
        self.assertTrue(os.path.exists(os.path.join(os.curdir, "{}.json".format(self.test_project_id))))

    def test_can_get_project_id_from_url(self):
        """
        测试几种情况下都能够正确获取项目 id
        :return:
        """
        project_id_length = len("53c49025d105401f5e0003ec")
        test_project_id = "".join([random.choice(string.hexdigits) for i in range(project_id_length)])

        # 情况5: 输入错误的项目 id, 会有异常抛出
        with self.assertRaises(RuntimeError):
            test_url = "21321{}1321321d1".format(test_project_id)
            self.test_atm_scrapy.get_project_id_from_url(test_url)

        # 情况1: 直接传项目 id
        test_url = test_project_id
        self.assertEqual(self.test_atm_scrapy.get_project_id_from_url(test_url), test_project_id)

        # 情况2: 复制 url 传入
        test_url = "http://200.200.0.33/atm/projects/{}".format(test_project_id)
        self.assertEqual(self.test_atm_scrapy.get_project_id_from_url(test_url), test_project_id)

        # 情况3: 复制 url, 但多了个末尾的 /
        test_url = "http://200.200.0.33/atm/projects/{}/".format(test_project_id)
        self.assertEqual(self.test_atm_scrapy.get_project_id_from_url(test_url), test_project_id)

        # 情况4: 复制 url, 但多了一大串后缀, 比如 /suites
        test_url = "http://200.200.0.33/atm/projects/{}/suites".format(test_project_id)
        self.assertEqual(self.test_atm_scrapy.get_project_id_from_url(test_url), test_project_id)

    def test_can_parse_json_to_a_dict(self):
        """
        虽然 json 库已经帮我们封装好了操作, 不过这里还是要验证一下(虽然测试原则不让这么做)
        :return:
        """
        a_dict = self.test_atm_scrapy.parse_tree_json_file("{}.json".format(self.test_project_id))
        self.assertTrue(isinstance(a_dict, dict))

        self.assertEqual(a_dict[0]["name"] == "必选发布测试项new")
        self.assertEqual(a_dict[1]["name"] == "储运母盘测试(适用于32G SSD)")

    def test_can_create_dir_from_a_dict(self):
        """
        现在已经有一个被 json 解析好的字典了, 验证是否能够从这个字典创建文件夹
        :return:
        """
        a_dict = self.test_atm_scrapy.parse_tree_json_file("{}.json".format(self.test_project_id))
        self.test_atm_scrapy.create_dirs_from_dict(a_dict)

        parent_dirs = ["必选发布测试项new", "储运母盘测试(适用于32G SSD)"]
        self.assertTrue(all(os.path.exists(os.path.join(os.curdir, parent_dir)) for parent_dir in parent_dirs))

        children_dirs = ["前置", "新增异常处理机制", "国标测试", "IPv6功能-zwj", "新增20150908", "原发布测试项自动化", ""]
        self.assertTrue(all(
            os.path.exists(os.path.join(os.curdir, "储运母盘测试(适用于32G SSD)", children_dir)) for children_dir in
            children_dirs))

        test_dir = os.curdir
        for next_dir in ["必选发布测试项new", "发布测试项", "国标测试", "功能列表", "包过滤"]:
            test_dir = os.path.join(test_dir, next_dir)
            self.assertTrue(os.path.exists(test_dir))

    def test_can_get_all_cases_from_dir_id(self):
        """
        测试能够从一个文件夹的 id 获取到当前文件夹下的所有案例
        :return:
        """
        pass


if __name__ == "__main__":
    pass
