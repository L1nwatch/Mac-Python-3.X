#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 实现对指定文件夹下所有文件进行内容搜索, 关键词及搜索的文件类型由用户指定

2016.08.20 发现搜寻 GBK 编码的工程时中文注释不能完全搜索到, 编码方便的能力还是需要加强一下.
2016.08.13 发现打开不同编码时会出错, 需要加强一下编码方面的能力
2016.07.27 扩展一下搜索文件类型
2016.07.23 由于自己现在记的笔记形式是 GitHub + GitBook, 但是这两货的笔记搜索功能是在有限, 故需要将此程序进一步扩展
2016.06.21 由于微机原理也要进行 ARM 平台小车的开发, 遇到了跟 ZigBee 一样的困境, 需要快速掌握工程文件, 所以还是将这个程序通用化吧
2016.04 起初编写这个程序是由于对协议栈不熟悉, 所以需要对协议栈的每一个文件进行关键词搜索, 同时列举出来
"""
import os
import argparse
import chardet
import re
import platform

__author__ = '__L1n__w@tch'


def is_valid_file_type(name, types):
    """
    :param name: 文件名, 比如 '.DS_Store'
    :param types: 要搜寻的文件类型, 比如 [".h", ".c"]
    :return: False
    """
    name = name.lower()
    for each_type in types:
        if name.endswith(each_type):
            return True
    return False


def add_argument(parser, default_file_type):
    """
    为解析器添加参数
    :param default_file_type: 默认要搜索的文件类型, 格式比如: ".c#.h#.cpp#.py#.md"
    :param parser: ArgumentParser 实例对象
    :return: None
    """
    parser.add_argument("--path", "-p", type=str,
                        default=os.curdir, help="文件夹路径")
    parser.add_argument("--type", "-t", type=str, default=default_file_type,
                        help="搜索文件类型, 默认值及格式为: \"{}\"".format(default_file_type))
    parser.add_argument("--keyword", "-k", type=str, default="main", help="要搜索的关键词")


def set_argument(options):
    """
    读取用户输入的参数, 检验是否合法
    :param options: parser.opts
    :return: dict()
    """
    configuration = dict()
    configuration["path"] = options.path
    configuration["file_type"] = options.type.split("#")
    # configuration["keyword"] = options.keyword.lower()

    print("[*] 要搜索的路径为: {}".format(configuration["path"]))
    print("[*] 要搜索的文件类型包括: {}".format(configuration["file_type"]))
    # print("[*] 要搜索的关键词为: {}".format(configuration["keyword"]))

    return configuration


def initialize(default_file_type=".h#.c#.cpp#.pl"):
    """
    进行初始化操作, 包括 argparse 解析程序的初始化, 参数的相关设定等
    :return: path, file_type, keyword
    """
    parser = argparse.ArgumentParser(description="文件内容搜索程序")
    add_argument(parser, default_file_type)
    configuration = set_argument(parser.parse_args())

    print("[*] {} 搜索开始 {}".format("-" * 30, "-" * 30))

    return configuration["path"], configuration["file_type"]


def get_keyword(word, content):
    """
    使用正则表达式进行搜索匹配
    :param word: "keyword"
    :param content: "first line \nheiheiehei keywordsecond line\nthird line\n"
    :return: heiheiehei keywordsecond line\n
    """
    if "\r" in content:
        result = re.search("[^\r\n]*({}[^\r\n]*\r?\n?)".format(word), content)
    else:
        result = re.search("[^\n]*({}[^\n]*\n?)".format(word), content)
    return result.group() if result else None


def search_keyword_infile(file_path, word):
    """
    判断一个文件内是否含有该关键词, 并且把含有该关键词的那一行返回回去
    :param file_path: 文件路径, 比如 './compare_key.py'
    :param word: "main"
    :return: 返回含有关键词的那一行, 或者返回 None 表示找不到, 即 None or "int main()"
    """
    # word 处理
    word = word.lower()

    with open(file_path, "rb") as f:
        data = f.read()
        encoding = chardet.detect(data)["encoding"]

    try:
        data = data.decode(encoding)
    except UnicodeDecodeError:
        data = data.decode("gbk")

    return get_keyword(word, data)


def decode_content(content):
    """
    给一定串字节流, 进行正确的解码操作
    :param content: b"aaa"
    :return: "aaa"
    """
    encoding = chardet.detect(content)["encoding"]
    return content.decode(encoding)


def is_windows_system():
    """
    判断运行程序的系统是否是 Windows 系统
    :return: True or False
    """
    return "window" in platform.platform()


if __name__ == "__main__":
    path, file_type = initialize()
    keyword = input("[?] 请输入要搜索的关键词: ")

    for root, dirs, files in os.walk(path):
        for each_file in files:
            if is_valid_file_type(each_file, file_type):
                path = root + os.sep + each_file
                line_content = search_keyword_infile(path, keyword)
                if line_content:
                    color1, color2, color3, color4 = "\033[95m", "\033[0m", "\033[91m", "\033[0m"
                    if is_windows_system():
                        color1, color2, color3, color4 = None
                    print("[!] Found in \"{}\", path is {color1}{path}{color2}"
                          .format(each_file, path=path, color1=color1, color2=color2))
                    print("[!] {}{color3}{content}{color4}"
                          .format("\t" * 4, color3=color3, content=line_content.strip(), color4=color4))
    print("[*] {} 搜索结束 {}".format("-" * 30, "-" * 30))
    input("输入任意键退出")
