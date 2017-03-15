#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""数据源是类 xml 但又不是 xml 的文件, 真坑, 按照文本流的方式进行处理之后转成 json 吧

2017.03.15 将类 xml 的数据转换为一个一个 json 文件
"""
try:
    import simplejson as json
except ImportError:
    import json
import os
import codecs
import re

__author__ = '__L1n__w@tch'


def parse_doc_to_dict(doc_content):
    """
    将一段 doc 解析成字典形式
    :param doc_content: str(), 每个 doc 段, 比如 "<doc>....</doc>"
    :return: dict(), 解析后的 dict 形式, 比如 {"url": xxx, "doc_number": xxx, "content_title": xxx, "content": xxx}
    """
    result_dict = dict()

    url_tag_re = re.compile("<url>([\s\S]*?)</url>", flags=re.IGNORECASE)
    doc_number_re = re.compile("<docno>([\s\S]*?)</docno>", flags=re.IGNORECASE)
    content_title_re = re.compile("<contenttitle>([\s\S]*?)</contenttitle>", flags=re.IGNORECASE)
    content_re = re.compile("<content>([\s\S]*?)</content>", flags=re.IGNORECASE)

    result_dict["url"] = url_tag_re.findall(doc_content)[0]
    result_dict["doc_number"] = doc_number_re.findall(doc_content)[0]
    result_dict["content_title"] = content_title_re.findall(doc_content)[0]
    result_dict["content"] = content_re.findall(doc_content)[0]

    return result_dict


def get_docs_from_file(file_name):
    """
    作为生成器, 读取文件里的每一个段
    :param file_name: str(), 文件名, 比如 "news_tensite_xml.smarty.dat"
    :return: str(), 读取出来的每个 doc 段, 比如 "<doc>....</doc>"
    """
    with open(file_name, "rb") as f:
        doc_content = str()

        for each_line in f:
            each_line = codecs.decode(each_line, "gb18030", "strict")
            doc_content += each_line

            if each_line == "</doc>\n":
                yield doc_content
                doc_content = str()


def run(file_name):
    """
    实现 xml2json 的功能
    :param file_name: str(), xml 源文件名称
    :return: None, 创建一个一个 json 文件而已
    """
    dir_path = "xml2json_result"
    os.makedirs(dir_path, exist_ok=True)

    # 按 doc 读取文件
    for i, each_doc in enumerate(get_docs_from_file(file_name)):
        doc_dict = parse_doc_to_dict(each_doc)

        with codecs.open(os.path.join(dir_path, "news_data{}.json".format(i)), "w") as f:
            json.dump(doc_dict, f)


if __name__ == "__main__":
    data_file_name = "news_tensite_xml.smarty.dat"
    run(data_file_name)
