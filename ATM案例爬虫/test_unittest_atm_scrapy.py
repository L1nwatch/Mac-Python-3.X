#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.11.26 通过了好多单元测试,但是整体运行了之后感觉测试效率下降了,所以优化一下,在单元测试里面就只爬一次
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
    @classmethod
    def setUpClass(cls):
        cls.test_project_id = "53c49025d105401f5e0003ec"

        # 创建测试时所下载的东西会保存的路径
        cls.test_path = os.path.join(os.path.abspath(os.curdir), "test_for_crawl")
        os.makedirs(cls.test_path, exist_ok=True)

        # 爬虫操作
        cls.test_atm_scrapy = ATMScrapy(path_dir=cls.test_path, url=cls.test_project_id)

    def test_can_download_json_file_from_project_id(self):
        """
        测试给定一个项目id, 能够下载到 json 文件并命名为 id.json
        :return:
        """
        response = self.test_atm_scrapy.download_tree_json_file(self.test_project_id)
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
        a_list = self.test_atm_scrapy.parse_tree_json_file("{}.json".format(self.test_project_id))
        self.assertTrue(isinstance(a_list, list))

        self.assertEqual(a_list[0]["name"], "必选发布测试项new")
        self.assertEqual(a_list[1]["name"], "储运母盘测试(适用于32G SSD)")

    def test_can_create_dir_from_a_dict(self):
        """
        现在已经有一个被 json 解析好的 list 了, 验证是否能够从这个 list 创建文件夹/文件
        :return:
        """
        # 初始化爬虫及方法所需的参数
        # TODO: 测试的内容还是太多, 导致测试太慢
        a_list = self.test_atm_scrapy.parse_tree_json_file("json_file_for_test.json")

        # 调用方法
        self.test_atm_scrapy.create_case_trees_from_list(a_list, self.test_path)

        # 测试俩根目录
        parent_dirs = ["必选发布测试项new", "储运母盘测试(适用于32G SSD)"]
        self.assertTrue(all(os.path.exists(os.path.join(self.test_path, parent_dir)) for parent_dir in parent_dirs))

        children_dirs = ["前置", "新增异常处理机制", "国标测试", "IPv6功能-zwj", "新增20150908", "原发布测试项自动化"]
        self.assertTrue(all(
            os.path.exists(os.path.join(self.test_path, "储运母盘测试(适用于32G SSD)", children_dir)) for children_dir in
            children_dirs))

        test_dir = self.test_path
        for next_dir in ["必选发布测试项new", "发布测试项", "国标测试", "功能列表", "包过滤"]:
            test_dir = os.path.join(test_dir, next_dir)
            self.assertTrue(os.path.exists(test_dir))

    def test_can_get_all_cases_from_dir_id(self):
        """
        测试能够从一个文件夹的 id 获取到当前文件夹下的所有案例
        :return:
        """
        cases = ["前置-登录设备绕过前台加密", "前置-环境整理", "前置-文件拷贝", "前置-网络部署"]
        root_dirs = ["预发布项自动化案例", "发布测试项-6.8-7.0", "前置--请手动清理设备环境"]

        test_path = "{}/{}".format(self.test_path, "/".join(root_dirs))
        test_cases_id = "57eb3d9ed10540526e00116f"
        os.makedirs(test_path, exist_ok=True)

        self.test_atm_scrapy.create_cases_from_cases_id(test_cases_id, test_path)

        self.assertTrue(all(os.path.exists(os.path.join(test_path, each_case)) for each_case in cases))

    def test_can_get_case_content_from_case_id(self):
        """
        给定一个案例 id, 能够获取到其全部内容
        :return:
        """
        with open("case_content_for_test.txt", "r") as f:
            right_content = f.readlines()
            right_content = [x.strip() for x in right_content]  # 清除换行符差异

        result = self.test_atm_scrapy.get_case_content_from_case_id("55c96a76d105400f411a1e74")
        result = result.splitlines()  # 清除换行符差异

        self.assertEqual(right_content, result)


if __name__ == "__main__":
    pass
