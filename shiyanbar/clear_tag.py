#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 用于清除文件中的某一指定标签
'''
__author__ = '__L1n__w@tch'

import re


def delete_pairs_tags(response, html_tag="script"):
    """
    清除成对的标签及其中的内容

    :param response: "3.1 打开Brute Froce页面，在页面的最下方点击View Source。。查看源代码。如图11所示
<center>![](/UploadImage/2016/1/4/20_95653)</center><center>图 11</center>"
    :param html_tag: "center"
    :return: "3.1 打开Brute Froce页面，在页面的最下方点击View Source。。查看源代码。如图11所示"
    """
    response = re.sub(r"</{0}>".format(html_tag), r"<{0}>".format(html_tag), response)
    response = re.sub(r"<{0}[^>]*?>[\s\S]*?<{0}[^>]*?>".format(html_tag), "", response)
    return response


def main():
    file_name = "wait_to_delete"
    with open(file_name, "r") as f:
        data = f.read()
        data = delete_pairs_tags(data, "center")

    with open(file_name, "w") as f:
        f.write(data)


if __name__ == "__main__":
    main()
