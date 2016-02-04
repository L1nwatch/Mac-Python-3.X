#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' sax解析xml
'''
__author__ = '__L1n__w@tch'

import xml.sax
import xml.sax.handler


class ToolHireHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        super().__init__()
        self.dates = list()
        self.date_lent = str()
        self.date_counter = 0
        self.is_date = False

    # Override,注意保持名称一致
    def startElement(self, name, attributes):
        """
        主要的解析方法是startElement()方法,它会寻找Data元素,一旦发现,它会通过只选择那些ss:Type特性为DateTime的元素来优化搜索
        :param name:
        :param attributes:
        :return:
        """
        if name == "Data":
            data = attributes.get("ss:Type", None)
            if data == "DateTime":
                self.is_date = True
                self.date_counter += 1
            else:
                self.date_counter = 0

    # Override,注意保持名称一致
    def endElement(self, name):
        """
        endElement()方法保证self.is_date标签被重置为False,为下一个将要到来的startElement()事件做准备
        :param name:
        :return:
        """
        self.is_date = False

    # Override,注意保持名称一致
    def characters(self, data):
        """
        无论何时碰到标签外面的内容,character()方法都会被调用.
        :param data:
        :return:
        """
        if self.is_date:
            if self.date_counter == 1:
                self.date_lent = data
            else:
                self.dates.append((self.date_lent, data))


def main():
    """
    驱动代码创建了处理程序和解析器实例,然后将解析器中的处理程序设置为ToolHireHandler实例并对XML文件执行parse()操作.
    在解析完成之后,它打印出从处理程序获得的日期
    :return:
    """
    handler = ToolHireHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    parser.parse("toolhire.xml")
    print(handler.dates)


if __name__ == "__main__":
    main()
