#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 以doctest模块进行简单测试

注意: doctest会要求代码缩进.第一行代码的缩进决定后续的缩进,所以需要遵循这个缩进模式.
doctest字符串会像编写的那样精确地传入解释器——如果解释器期待一个特定的缩进,则需要确保doctest字符串是符合那个缩进模式的
同时要记住的是,随着Python的改变和进化,缩进模式可能会改变,所以doctest字符串可能在将来不可用.这就是为什么许多人在很重要的测试中不
很依赖于doctest的原因之一

doctest 不适合测试大的、复杂的方法或函数.但是,它非常擅长"约定编程(contract programming)".通过使用doctest字符串并给约定就可以进
行测试.然而,不能测试所有可能的输出,所以doctest在较大项目中很快就会遇到瓶颈问题

在终端中输入命令:
python -m doctest -v simple_doctest.py
通过传递一个-m标签,告诉Python你想要使用一个模块来执行文件.
而-v标签意味着你想要完整的输出, 比如:
Trying:
    simple_math(1, 2)
Expecting:
    3
ok
Trying:
    simple_math('k', 'v')
Expecting:
    'kv'
ok
Trying:
    sq(3)
Expecting:
    9
ok
2 items had no tests:
    test_doctest
    test_doctest.main
2 items passed all tests:
   2 tests in test_doctest.simple_math
   1 tests in test_doctest.sq
3 tests in 4 items.
3 passed and 0 failed.
Test passed.

'''
__author__ = '__L1n__w@tch'

import doctest


# 有时,需要测试一个不能一直保持一致的预测值,比如说内存地址
class SimpleClass():
    pass


# 其实,你并不在乎内存地址,你只在乎被创建的对象,ELLIPSIS选项让doctest知道之后的内容可以是任意值
# 如果正在检查是否返回了一个列表,ELLIPSIS常量也同样有用,比如当使用range()方法时.比如说,你想要确保当
# 调用range(4589)时,得到了数字1-4590.可以使用ELLIPSIS常量并只是设置你的结果为[0,1,...,4588,4589],
# 而不是打印整个4590个数字的整个列表.
def class_testing_method_ahoy(obj):
    """
    Should return a list containing the object

    >>> class_testing_method_ahoy(SimpleClass()) # doctest: +ELLIPSIS
    [<test_doctest.SimpleClass object at 0x...>]

    :param obj:
    :return:
    """
    return [obj]


def sq(n):
    """
    this function should take in a number and return its squared value
    >>> sq(3)
    9

    注意这里要空一行来区分一下输出
    :param n:
    :return:
    """
    return n * n


def simple_math(x, y):
    """
    为了进行测试,必须在解释器提示符(>>>)后有一个空格.
    >>> simple_math(1, 2)
    3

    >>> simple_math('k', 'v')
    'kv'

    :param x:
    :param y:
    :return:
    """
    return x + y


def main():
    pass


if __name__ == "__main__":
    main()
