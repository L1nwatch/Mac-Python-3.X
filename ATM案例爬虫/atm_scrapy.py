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
        pass


if __name__ == "__main__":
    atm_project_url = "http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec/suites"
    case_url = "http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec/suites?id=57eb3d9ed10540526e00116f"
    atm_scrapy = ATMScrapy()
    atm_scrapy.crawl(atm_project_url)
    atm_scrapy.crawl(case_url)
    print("\u524d\u7f6e-\u767b\u5f55\u8bbe\u5907\u7ed5\u8fc7\u524d\u53f0\u52a0\u5bc6")

"""
分析数据:
designer_ztree_2976_a   http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec/usecases/582 92d13 d10540 0b46 000 0b1
designer_ztree_2976_a   582 92d13 d10540 0b46 000 0b1
designer_ztree_2977_a   582 3de25 d10540 182c 000 10d
designer_ztree_2978_a   582 3e540 d10540 6c5e 000 090
designer_ztree_2979_a   582 ac21b d10540 6b97 000 066
designer_ztree_2980_a   582 aced0 d10540 795a 000 039
designer_ztree_2981_a   582 c2d84 d10540 5b14 000 07e

designer_ztree_1_a      http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec/usecases/statistics?suite_id=55c96a08d105400f27067a23
designer_ztree_1_a      55c96a08d105400f27067a23
designer_ztree_2_a      55c96a75d105406a8a02d808
designer_ztree_3_a      55c96a75d105400f411a1e73
designer_ztree_2913_a   55c96a76d105400f411a1e74
designer_ztree_2914_a   55c96a76d105400f411a1ebc
designer_ztree_2915_a   57dbc983d10540692e000070
designer_ztree_4_a      56946a1dd1054047b2000008
designer_ztree_2916_a   56946a67d1054046d100000b
designer_ztree_5_a      55c96a78d105400f411a1fd0
designer_ztree_6_a      55c96a78d105400f411a1fd1
designer_ztree_7_a      55c96a78d105400f411a1fd2
designer_ztree_2917_a   55c96a79d105400f411a2016    前置-准备执行主机环境     9行          -- 66   ;len = 809
designer_ztree_2918_a   55c96a79d105400f411a2058    134920TCP协议访问控制     7行         -- 35    ;len = 446
designer_ztree_2919_a   55c96a79d105400f411a207b    134921UDP协议访问控制     11-12行      -- 46   ;len = 663
designer_ztree_2920_a   55c96a79d105400f411a20a9    134915默认禁止原则        30-33行      -- 125  ;len = 1867
designer_ztree_2921_a   55c96a79d105400f411a2126    134917目的IP访问控制       17 行       -- 87   ;len = 1203
designer_ztree_2922_a   55c96a7ad105400f411a217d    134919目的端口访问控制      12 行        -- 62  ;len = 803
designer_ztree_2923_a   55c96a7ad105400f411a21bb    134916源IP地址访问控制      17 行(18行为空) -- 85  ;len = 1133
designer_ztree_2924_a   55c96a7ad105400f411a2210    134918源端口访问控制        8 行        -- 51   ;len = 559
designer_ztree_2925_a   55c96a7ad105400f411a2243    后置-清理环境               10 行
"""
