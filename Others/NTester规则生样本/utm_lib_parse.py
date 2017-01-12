#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.11 UTM 的不是用解析 pcap 包的方式来搞的, 所以还是新建个脚本来专门处理吧
"""
try:
    import simplejson as json
except ImportError:
    import json

import svn.remote
import os

__author__ = '__L1n__w@tch'


# TODO: 三个 entry 文件拿下来
# TODO: 解密三个 entry 文件
# TODO: 解析解密后的文件

class UTMParser:
    def __init__(self, svn_information):
        self.svn_url, self.svn_user, self.svn_passwd, self.checkout_path = svn_information

    def get_latest_utm_urls(self, target_path):
        """
        利用 svn 下载到最新的 utm 明文 url 信息
        :param target_path: str(), 要将东西 checkout 到哪里?
        """
        r = svn.remote.RemoteClient(self.svn_url, username=self.svn_user, password=self.svn_passwd)
        r.checkout(target_path)  # 包括了 checkout 及 update, 很不错

    @staticmethod
    def extract_urls(url_file):
        """
        读取 url 文件, 把其中的所有 URL 提取出来, 通过按行读取实现
        :return:
        """
        result_set = set()

        with open(url_file, "r") as f:
            data = f.read()

        for each_line in data.splitlines():
            if each_line != "N/A" and each_line != "":
                result_set.add(each_line)
        return result_set

    def get_all_utm_urls(self, root_path):
        """
        读取每一个 url_add.txt 文件, 将其中的 url 提取出来存到一个 list 中, 并返回
        :param root_path: urls 文件的根目录, 会遍历该目录读取每一个 url_add
        :return: set(), 里面保存所有 url
        """
        urls_set = set()

        for root, dirs, files in os.walk(root_path):
            for each_file in files:
                if each_file == "url_add.txt":
                    file_path = os.path.join(root, each_file)
                    urls_set.update(self.extract_urls(file_path))

        return list(urls_set)

    def run(self, result_json_path):
        """
        完成 UTM 解析的全套流程
        """
        print("[*] 开始 checkout UTM 库最新 URL 信息")
        self.get_latest_utm_urls(self.checkout_path)

        print("[*] 开始提取所有 URL")
        urls_list = self.get_all_utm_urls(self.checkout_path)

        print("[*] 保存 url 提取结果到 {}".format(result_json_path))
        with open(result_json_path, "w") as f:
            json.dump(urls_list, f)


if __name__ == "__main__":
    svn_info = ("https://200.200.0.8/svn/test/测试部文件服务器/测试工程/AF版本/AF规则/UTM规则验证/",
                "linfeng", "lf123456", "./utm_urls_lib")
    utm_parser = UTMParser(svn_info)
    utm_parser.run("utm_url_result.json")
