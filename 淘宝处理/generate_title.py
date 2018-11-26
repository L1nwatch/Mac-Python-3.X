#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 输入核心词,输入一堆关联词,生成指定数量的标题
"""
import random

__author__ = '__L1n__w@tch'


def generate_title(core_word, attribute_word):
    """
    根据核心词,属性词生成标题
    :param core_word:
    :param attribute_word:
    :return:
    """
    result = [core_word]
    while len("".join(result)) < 30:
        pack_word = random.choice(attribute_word)
        if pack_word not in result:
            if (len("".join(result)) + len(pack_word)) > 30:
                break
            result.insert(random.randint(0, len(result)), pack_word)
    return "".join(result)


if __name__ == "__main__":
    core_word = "坐垫"
    attribute_word = [
        "坐凳", "坐椅", "家用", "秋冬", "加厚",
        "男女", "宿舍", "屁股垫", "艾灸", "艾绒",
        "汽车", "沙发", "旅行", "板凳", "地上",
        "学生", "长方形", "四季", "办公",
    ]

    # 要生成 20 个左右标题
    all_titles = set()
    for i in range(20):
        all_titles.add(generate_title(core_word, attribute_word))

    print("[*] 总共生成了 {} 个标题".format(len(all_titles)))
    for each_title in all_titles:
        print(each_title)
