#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.12.01 爬虫在 Windows 下运行遇到了编码错误, 只好专门拿出来调试了
"""
import os
import atm_scrapy
import codecs

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    project_url = "53c49025d105401f5e0003ec"
    debug_json_file = "57eb931cd10540526e018afc.json"
    debug_dir = "debug_encoding"
    os.makedirs(debug_dir, exist_ok=True)

    debug_atm_crawl = atm_scrapy.ATMScrapy(project_url)

    name = "{}.txt".format(debug_atm_crawl.get_safe_name("debug_test_case_txt"))
    case_file_path = os.path.join("./{}".format(debug_dir), name)
    case_content = debug_atm_crawl.get_case_content_from_case_id("583be601d1054076520000e1")

    try:
        with open(case_file_path, "w") as f:
            f.write(case_content)
    except UnicodeEncodeError as e:
        with open(case_file_path, "w", encoding="utf8") as f:
            f.write(case_content)
