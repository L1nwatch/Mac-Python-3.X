#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
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

    def test_can_get_case_names(self):
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




if __name__ == "__main__":
    pass
