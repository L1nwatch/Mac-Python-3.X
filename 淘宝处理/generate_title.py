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
    core_word = "棉拖鞋"
    attribute_word = [
        "女", "秋冬", "毛毛", "男", "可爱",
        "月子", "情侣", "居家", "包跟", "室内",
        "毛绒", "卡通", "厚底", "保暖", "防滑",
        "家用", "韩版", "卧室", "百搭","公主"
    ]

    # 要生成 20 个左右标题
    all_titles = set()
    for i in range(20):
        all_titles.add(generate_title(core_word, attribute_word))

    print("[*] 总共生成了 {} 个标题".format(len(all_titles)))
    for each_title in all_titles:
        print(each_title)
