#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 输入核心词,输入一堆关联词,生成指定数量的标题
"""
import copy
import random

__author__ = '__L1n__w@tch'


def generate_title(core_word, attribute_word):
    """
    根据核心词,属性词生成标题
    :param core_word:
    :param attribute_word:
    :return:
    """
    attribute_word = copy.deepcopy(attribute_word)
    result = [core_word]
    while len("".join(result)) < 30:
        if len(attribute_word) <= 0:
            break
        pack_word = random.choice(attribute_word)
        attribute_word.remove(pack_word)
        if pack_word not in result:
            if (len("".join(result)) + len(pack_word)) > 30:
                break
            result.insert(random.randint(0, len(result)), pack_word)
    return "".join(result)


if __name__ == "__main__":
    core_word = "浴室地毯"
    attribute_word = [
        "地垫", "卧室", "脚垫", "防滑", "进门",
        "家用", "卫生间", "吸水", "厕所", "门口",
        "方块", "欧式", "阳台", "美式", "宿舍",
        "灰色", "毛绒", "茶几", "儿童", "防水", "淋浴",
        "门外", "入户", "进门", "卫浴"
    ]

    # 要生成 20 个左右标题
    all_titles = set()
    for i in range(20):
        all_titles.add(generate_title(core_word, attribute_word))

    print("[*] 总共生成了 {} 个标题".format(len(all_titles)))
    for each_title in all_titles:
        print(each_title)
