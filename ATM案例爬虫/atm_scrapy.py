#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.11.26 陆续编写, 到今天终于可以完成下载功能了, 简称爬虫 v1.0
2016.11.20 发现 ATM 本身就提供导出案例的功能, 不过是导出成 excel 格式的
2016.11.16 爬虫, 爬取公司上的 ATM 平台的案例, 要不然学习别人的案例学习起来不方便
"""
import requests
import os
import re
import datetime
from my_constant import const

try:
    import simplejson as json
except ImportError:
    import json

__author__ = '__L1n__w@tch'


class ATMScrapy:
    def __init__(self, url, path_dir=os.curdir):
        self.project_id = self.get_project_id_from_url(url)
        print("开始爬, 目标项目:{}".format(self.project_id))

        # 初始化默认下载目录
        if path_dir == os.curdir:
            today = datetime.datetime.now()
            self.path_dir = os.path.join(path_dir, "ATM爬虫:{year}{month}{day}-{hour}{minute}".format(
                year=today.year, month=today.month, day=today.day,
                hour=str(today.hour).zfill(2), minute=str(today.minute).zfill(2)))

        os.mkdir(path_dir) if not os.path.exists(path_dir) else None

    def crawl(self):
        """
        执行整体爬虫流程
        :return:
        """
        # 下载并解析 json 文件
        json_file_path = self.download_tree_json_file()
        parse_result = self.parse_tree_json_file(json_file_path)

        # 创建对应文件夹/文件, 并保存 id 号
        result = self.create_case_trees_from_list(parse_result)

        os.remove(json_file_path)

        print("项目{}:{}".format(self.project_id, result))
        return result

    def download_tree_json_file(self, project_id=None):
        """
        下载整体的 json 文件
        :param project_id: 项目的 id
        :return:
        """
        if project_id is None:
            project_id = self.project_id
        response = requests.get(url="http://200.200.0.33/atm/projects/{}/suites".format(project_id))

        json_file_path = "{}.json".format(self.project_id)
        with open(json_file_path, "w") as f:
            f.write(response.text)

        return json_file_path

    @staticmethod
    def get_project_id_from_url(url):
        """
        从给定的 url 中解析出项目 id
        :param url: "http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec"
        :return: "53c49025d105401f5e0003ec"
        """
        project_id = re.findall(".*([0-9a-zA-Z]{24}).*", url)[0]
        all_possible_id = re.findall("([0-9a-zA-Z]*)", url)
        if all(possible_id != project_id for possible_id in all_possible_id):
            raise RuntimeError
        return project_id

    @staticmethod
    def parse_tree_json_file(file_path):
        """
        负责解析 json 文件并且创建对应文件夹及文件
        :param file_path:
        :return:
        """
        with open(file_path, "r") as f:
            result = json.load(f)

        return result

    def create_case_trees_from_list(self, a_list, path_dir=None):
        """
        根据一个列表创建对应的文件夹, 文件
        :param a_list: json 格式的一个列表
        :param path_dir: 下载文件夹的根目录
        :return:
        """
        if path_dir is None:
            path_dir = self.path_dir

        def __recursion_create_dirs(children_list, root_path):
            for each_kid in children_list:
                path = os.path.join(root_path, each_kid["name"])
                os.makedirs(path, exist_ok=True)

                print("下载{}中...".format(each_kid["name"]))

                # 不是最后一级目录
                if len(each_kid["children"]) > 0:
                    __recursion_create_dirs(each_kid["children"], path)
                # 已经是最后一级目录了
                else:
                    self.create_cases_from_cases_id(each_kid["id"], path)

        __recursion_create_dirs(a_list, path_dir)

        return const.SUCCESS_MESSAGE

    def create_cases_from_cases_id(self, cases_id, path):
        """
        根据字典, 在不同文件夹下创建对应的案例
        :param cases_id: cases 的 id, 通过这个 id 可以获取到这个文件夹下的所有案例
        :param path: 要放置的目录
        :return:
        """
        url = "http://200.200.0.33/atm/projects/{}/suites?id={}".format(self.project_id, cases_id)

        # 获取最后一级目录中所有案例 id, 保存到 json 中
        response = requests.get(url)
        json_file_path = "{}.json".format(cases_id)
        with open(json_file_path, "w") as f:
            f.write(response.text)

        # 解析保存的 json 文件, 创建对应案例
        a_list = self.parse_tree_json_file(json_file_path)
        for each_case in a_list:
            case_file_path = os.path.join(path, "{}".format(each_case["name"]))
            with open(case_file_path, "w") as f:
                f.write(self.get_case_content_from_case_id(each_case["id"]))

        os.remove(json_file_path)

    def get_case_content_from_case_id(self, case_id):
        """
        给定一个 id, 获取其内容后返回
        :param case_id: "5832d192d105400a3100006e"
        :return: 案例的内容, str 形式
        """
        case_content_url = "http://200.200.0.33/atm/projects/{}/usecases/{}".format(self.project_id, case_id)
        response = requests.get(case_content_url)

        return response.text


if __name__ == "__main__":
    # atm_project_url = "http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec/suites"
    # case_url = "http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec/suites?id=57eb3d9ed10540526e00116f"
    # case_content = "http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec/usecases/5832d192d105400a3100006e"
    test_project_id = "53c49025d105401f5e0003ec"
    my_atm_crawl = ATMScrapy(test_project_id)
    my_atm_crawl.crawl()
