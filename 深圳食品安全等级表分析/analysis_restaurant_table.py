#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 分析深圳市 A 级餐厅名单
"""
import pandas
import re

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    restaurant = {"金拱门|金供门|麦当劳": 0, "幼儿园|幼教": 0, "小学": 0, "公安局|军供站|公安分局": 0, "高中": 0, "学校": 0, "探鱼": 0, "医院": 0,
                  "大学": 0, "中学": 0, "七十九号渔船": 0, "海底捞": 0, "学院": 0, "必胜客": 0, "面点王": 0, "肯德基": 0, "食堂": 0,
                  "真功夫": 0, "星巴克": 0, "永和大王": 0, "元绿迴转寿司|元气寿司": 0, "红荔村": 0, "乐凯撒|乐凯撤": 0, "润园四季": 0, "汉堡王": 0, "监狱": 0,
                  "捞王": 0, "八合里": 0, "酒店|酒楼": 0, "春满园": 0, "嘉旺": 0, "西贝": 0, "四季椰林": 0, "鑫辉": 0, "美西西|喜茶": 0,
                  "江南厨子|西湖春天": 0, "汉阳馆": 0, "蔡澜": 0, "家乐缘": 0, "百岁村|维也纳": 0, "阿里郎": 0, "金皇廷": 0, "大秦小宴": 0, "胜记": 0,
                  "野妹": 0, "萨莉亚": 0, "汉拿山": 0, "爱人餐饮": 0}
    not_classify_count = 0

    with open("9014821.csv", encoding="utf8") as f:
        data = pandas.read_csv(f)

        for name in data["单位名称"]:
            key_name = name
            not_classify_count += 1
            for each_key in restaurant.keys():
                if len(re.findall(each_key, name)) > 0:
                    key_name = each_key
                    not_classify_count -= 1
                    break
            restaurant[key_name] = restaurant.get(key_name, 0) + 1

        for key, value in restaurant.items():
            print(f"{key}---{value}")
        print(f"[*] 有 {not_classify_count} 家餐厅未被索引")
