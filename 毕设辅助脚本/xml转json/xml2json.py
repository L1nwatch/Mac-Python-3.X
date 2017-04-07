#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""数据源是类 xml 但又不是 xml 的文件, 真坑, 按照文本流的方式进行处理之后转成 json 吧

2017.04.07 增加域名解析的操作, 进行评测分析需要用到
2017.03.18 处理一下全角字符的问题
2017.03.17 区分一下 demo 数据和完整数据, 脚本运行结果分别保存在两个不同的地方
2017.03.16 增加两步操作, 把不可读的两个字符单独替换掉了
2017.03.15 将类 xml 的数据转换为一个一个 json 文件
"""
try:
    import simplejson as json
except ImportError:
    import json
import os
import codecs
import re
import unicodedata
import urllib.parse

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


def deal_with_wrong_char_with_lib(raw_data):
    """
    使用标准库处理错误字符
    :param raw_data: str(), 原始字符串, 可能包含错误字符, 比如 "abc９ｑ"
    :return: str(), 处理错误字符之后的结果, 比如 "abc9q"
    """
    return unicodedata.normalize("NFKC", raw_data).replace("", "")


def __deal_with_wrong_char_by_myself(raw_data):
    """
    测试后发现这个方法很慢, 所以还是用库方法吧
    import timeit

    def performSearch(array):
        array.sort()


    arrayTest = ["X"]*1000

    if __name__ == "__main__":
        print timeit.timeit("performSearch(arrayTest)","from __main__ import performSearch, arrayTest",number=10)

    自己遍历每个字符, 处理错误字符
    :param raw_data: str(), 原始字符串, 可能包含错误字符, 比如 "abc９ｑ"
    :return: str(), 处理错误字符之后的结果, 比如 "abc9q"
    """
    result = str()
    for each_char in raw_data:
        if each_char == "　":
            result += " "
        elif each_char == "":
            result += ""
        else:
            # 全角转半角处理
            inside_code = ord(each_char)
            if inside_code == 0x3000:
                inside_code = 0x0020
            else:
                inside_code -= 0xfee0
            if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
                result += each_char
            try:
                result += chr(inside_code)
            except ValueError as e:
                print("[-] Error at {} -> {}".format(each_char, inside_code))
                result += each_char
    return result


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
            doc_content += deal_with_wrong_char_with_lib(each_line)

            if each_line == "</doc>\n":
                yield doc_content
                doc_content = str()


def run(file_name, demo=True):
    """
    实现 xml2json 的功能
    :param file_name: str(), xml 源文件名称
    :param demo: boolean(), True or False, 主要是区分 demo 数据与完整数据, 要保存在不同的路径
    :return: None, 创建一个一个 json 文件而已
    """
    dir_path = "xml2json_result" if not demo else "demo_xml2json_result"
    print("[*] 针对文件 {} 进行 xml2json 操作, 结果保存在 {}".format(file_name, dir_path))
    os.makedirs(dir_path, exist_ok=True)

    # 按 doc 读取文件
    for i, each_doc in enumerate(get_docs_from_file(file_name)):
        doc_dict = parse_doc_to_dict(each_doc)

        with codecs.open(os.path.join(dir_path, "news_data{}.json".format(i)), "w") as f:
            json.dump(doc_dict, f)

    print("[*] xml2json 完毕")


def count_domain(file_name, demo=True):
    """
    实现统计域名信息
    :param file_name: str(), xml 源文件名称
    :param demo: boolean(), True or False, 主要是区分 demo 数据与完整数据, 要保存在不同的路径
    :return: None, 直接把结果保存到文件当中
    """
    result_dict = dict()
    result_file_name = "{}domain_parse_result.json".format("demo_" if demo else "")
    print("[*] 针对文件 {} 进行域名解析操作, 结果会保存在 {}".format(file_name, result_file_name))

    # 按 doc 读取文件
    for i, each_doc in enumerate(get_docs_from_file(file_name)):
        print("[*] 正在处理第 {} 个, 总共 {} 个".format(i + 1, 1294234))
        # 得到 url, 提取域名
        doc_dict = parse_doc_to_dict(each_doc)
        url = doc_dict["url"]
        domain = extract_domain_from_url(url)

        # 保存到字典里
        result_dict[domain] = result_dict.get(domain, 0) + 1

    # 将统计结果保存为 json 文件
    with open(result_file_name, "w") as f:
        json.dump(result_dict, f)


def delete_sub_domain_from_json(demo=True):
    """
    解析 json 文件, 删除子域名信息, 只保留主域名
    :param demo: boolean(), True or False, 主要是区分 demo 数据与完整数据, 要保存在不同的路径
    :return: None, 直接把结果保存到文件当中
    """
    # 读取 json 文件
    data_json_name = "{}domain_parse_result.json".format("demo_" if demo else "")
    result_file_name = "{}delete_sub_domain.json".format("demo_" if demo else "")

    with open(data_json_name, "r") as f:
        data_dict = json.load(f)

    # 解析每一个域名, 只保留主域名
    result_dict = dict()
    for key, value in data_dict.items():
        if key.endswith("people.com.cn"):
            result_dict["people.com.cn"] = result_dict.get("people.com.cn", 0) + value
        elif key.endswith("cn.yahoo.com"):
            result_dict["cn.yahoo.com"] = result_dict.get("cn.yahoo.com", 0) + value
        elif key.endswith("news.sohu.com"):
            result_dict["news.sohu.com"] = result_dict.get("news.sohu.com", 0) + value
        elif key.endswith("news.163.com"):
            result_dict["news.163.com"] = result_dict.get("news.163.com", 0) + value
        elif key.endswith("news.ifeng.com"):
            result_dict["news.ifeng.com"] = result_dict.get("news.ifeng.com", 0) + value
        else:
            result_dict[key] = result_dict.get(key, 0) + value

    # 保存到 json 文件
    with open(result_file_name, "w") as f:
        json.dump(result_dict, f)


def extract_domain_from_url(url):
    """
    从 url 中提取域名
    :param url: str(), url, 比如: "http://news.sohu.com/20120612/n345428229.shtml"
    :return: str(), 提取到的域名, 比如 "news.sohu.com"
    """
    return urllib.parse.urlparse(url).netloc


if __name__ == "__main__":
    demo_run = False
    if demo_run:
        data_file_name = "news_tensite_xml.smarty.dat"
    else:
        data_file_name = "news_tensite_xml.dat"
    # run(data_file_name, demo=demo_run)
    # count_domain(data_file_name, demo=demo_run)
    delete_sub_domain_from_json(demo=demo_run)
