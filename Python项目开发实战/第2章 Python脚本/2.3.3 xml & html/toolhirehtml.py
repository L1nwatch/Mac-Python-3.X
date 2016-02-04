#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 重写了handle_starttag()、handle_endtag()和handler_data()方法.这些方法直接类似于XML的startElement、endElement和character方法
'''
__author__ = '__L1n__w@tch'

import html.parser


class ToolHireParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.dates = list()
        self.date_lent = str()
        self.is_date = False
        self.date_counter = 0

    def handle_starttag(self, name, attributes):
        """
        解析器很贴心地考虑了混合大小写HTML标签或将标签名转换为小写,所以你不需要担心这一点.
        同时,它也尽量让糟糕格式的HTML变得有意义,尽管它不是很完善而且非常糟糕的代码可以让它犯错
        :param name:
        :param attributes:
        :return:
        """
        if name == "td":
            for key, value in attributes:
                if key == "class" and value == "xl65":
                    self.is_date = True
                    self.date_counter += 1
                    break
        else:
            self.date_counter = 0

    def handle_endtag(self, name):
        self.is_date = False

    def handle_data(self, data):
        if self.is_date:
            if self.date_counter == 1:
                self.date_lent = data
            else:
                self.dates.append((self.date_lent, data))


def main():
    htm = open("sheet001.htm").read()
    parser = ToolHireParser()
    parser.feed(htm)
    print(parser.dates)


if __name__ == "__main__":
    main()
