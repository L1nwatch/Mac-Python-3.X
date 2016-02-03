#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 纯文本解析示例
'''
__author__ = '__L1n__w@tch'


def has_mary(a_line):
    print("We found: ", a_line)


def parse_text(the_text, a_pattern, function):
    for line in the_text.split("\n"):
        if a_pattern in line:
            function(line)


def main():
    text = """mary had a little lamb its fleece was white as snow and everywhere that mary went the lamb was sure to go"""
    parse_text(text, "mary", has_mary)


if __name__ == "__main__":
    main()
