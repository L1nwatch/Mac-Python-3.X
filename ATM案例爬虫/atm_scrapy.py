#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.11.20 发现 ATM 本身就提供导出案例的功能, 不过是导出成 excel 格式的
2016.11.16 爬虫, 爬取公司上的 ATM 平台的案例, 要不然学习别人的案例学习起来不方便
"""
import requests
import os
import re
from my_constant import const
from selenium import webdriver

__author__ = '__L1n__w@tch'


class ATMScrapy:
    def crawl(self, url, path_dir=os.curdir):
        """
        执行整体爬虫流程
        :param url:
        :return:
        """
        # 下载 json 文件
        #
        file_path = self.download_tree_json_file(url)
        self.parse_tree_json_file(file_path)

    def download_tree_json_file(self, url):
        """
        下载整体的 json 文件
        :param url:
        :return:
        """
        project_id = self.get_project_id_from_url(url)
        response = requests.get(url="http://200.200.0.33/atm/projects/{}/suites".format(project_id))
        with open("{}.json".format(project_id), "w") as f:
            f.write(response.text)
        return const.SUCCESS_MESSAGE

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

    def parse_tree_json_file(self, file_path):
        """
        负责解析 json 文件并且创建对应文件夹及文件
        :param file_path:
        :return:
        """
        return dict()

    def create_dirs_from_dict(self, a_dict):
        """
        根据一个字典创建对应的文件夹
        :param a_dict:
        :return:
        """
        pass


if __name__ == "__main__":
    atm_project_url = "http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec/suites"
    case_url = "http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec/suites?id=57eb3d9ed10540526e00116f"
    atm_scrapy = ATMScrapy()
    atm_scrapy.crawl(atm_project_url)
    atm_scrapy.crawl(case_url)
    print("\u524d\u7f6e-\u767b\u5f55\u8bbe\u5907\u7ed5\u8fc7\u524d\u53f0\u52a0\u5bc6")
