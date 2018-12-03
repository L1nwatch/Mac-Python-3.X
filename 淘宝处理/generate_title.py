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
    core_word = "枕套"
    attribute_word = [
        "纯棉", "枕头套", "成人", "单人", "学生", "男", "女", "全棉", "大号", "枕芯套",
        "一对装", "大码", "双人", "情侣", "卡通", "方形", "花边", "秋冬", "创意", "可拆", "拆洗"
        , "健康", "卧室", "替换"
    ]

    # 要生成 20 个左右标题
    all_titles = set()
    for i in range(20):
        all_titles.add(generate_title(core_word, attribute_word))

    print("[*] 总共生成了 {} 个标题".format(len(all_titles)))
    for each_title in all_titles:
        print(each_title)
