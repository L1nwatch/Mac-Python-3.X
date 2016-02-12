#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' gettext模块以及locale示例代码
'''
__author__ = '__L1n__w@tch'

import gettext
import locale as loc


def main():
    # set up the locale and translation mechanism
    #############################################
    loc.setlocale(loc.LC_ALL, "")
    # 动态地创建了将要使用的翻译文件的名字.只创建了一个英文翻译文件,所以可以硬编码这个名字
    file_name = "res/messages_{}.mo".format(loc.getlocale()[0][0:2])

    # 实例化了一个gettext.GNUTranslations对象并对此对象执行install()操作.这激活了函数_(),之后使用该函数包围所有需要翻译的字符串
    trans = gettext.GNUTranslations(open(file_name, "rb"))
    trans.install()

    # Now the main program with gettext markers
    ###########################################
    print(_("Hello World"))

    # 下一步是生成message.po模版文件.如果是在一个类UNIX的操作系统上,可以按如下方式运行工具xgettext
    # xgettext test_gettext.py
    # 注意:Windows上与UNIX工具相对应的是pygettext.py和msgfmy.py这两个

    # 现在应该在Python文件的同一文件夹找到一个messages.po文件.在你的文本编辑器中打开它,然后将字符串CHARSET替换为UTF-8
    # 并在底部的空字符串中插入"Hello World"的翻译,通常对于英语来说,你只需要重复同样的字符串(你还可以填充其他一些metadata字段)
    # 现在讲文件保存为messages_en.po

    # 接下来,创建res(保存资源的)文件夹.已经在Python脚本中指定了这个文件夹名称.虽然res并不是一个严格的名称,但它是一个很有道理的命名约定
    # 执行另一个名为msgfmg的工具,如下:msgfmt -o res/messages_en.mo messages_en.po
    # 注意不同文件的结尾!上面的代码创建了翻译文件,告诉gettext在执行脚本时读取这个文件

    # 现在已经准备好运行该示例了:python3 gettext_demo.py
    # 通过为每个语言重复执行xgettext之后的步骤,可以继续生成更多翻译文件


if __name__ == "__main__":
    main()
