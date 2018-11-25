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
    core_word = "手套"
    attribute_word = [
        "骑行", "情侣", "防风", "五指", "防寒",
        "户外", "运动", "开车", "汽车", "防水",
        "滑雪", "骑行", "棉", "保暖", "耐磨",
        "男", "女", "加绒", "防冻", "发热",
        "登山", "全指", "潮流"
    ]

    # 要生成 20 个左右标题
    all_titles = set()
    for i in range(20):
        all_titles.add(generate_title(core_word, attribute_word))

    print("[*] 总共生成了 {} 个标题".format(len(all_titles)))
    for each_title in all_titles:
        print(each_title)

