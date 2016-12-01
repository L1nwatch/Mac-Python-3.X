#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.01 爬虫在 Windows 下运行遇到了编码错误, 只好专门拿出来调试了
"""
import os
import atm_scrapy

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    project_url = "53c49025d105401f5e0003ec"
    debug_json_file = "57eb931cd10540526e018afc.json"
    debug_dir = "debug_encoding"
    os.makedirs(debug_dir, exist_ok=True)

    debug_atm_crawl = atm_scrapy.ATMScrapy(project_url)

    # 解析保存的 json 文件, 创建对应案例
    a_list = debug_atm_crawl.parse_tree_json_file(debug_json_file)
    for each_case in a_list:
        debug_atm_crawl.write_case_into_file(each_case, "./debug_encoding")
