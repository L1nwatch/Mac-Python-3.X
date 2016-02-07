#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import itertools as it


def tools_function():
    # count()函数与内置的range()函数的工作原理非常类似。但range()产生有限的数字
    # 而count()从开始点产生无限数字序列。增加的步长可以通过可选参数stepsize控制。
    for n in it.count(15, 2):
        if n < 40:
            print(n, end=" ")
        else:
            break

    # repeat()函数只是持续地或按照指定的次数重复它的参数.
    for n in range(7):
        print(next(it.repeat("yes ")), end=" ")
    print(list(it.repeat(6, 3)))

    # cycle()函数会反复不断地在输入序列上轮转.这对于为负载平衡或资源分配创建轮式迭代是非常有用的
    res1 = list()
    res2 = list()
    res3 = list()
    resources = it.cycle([res1, res2, res3])
    for n in range(30):
        res = next(resources)
        res.append(n)
    print(res1)
    print(res2)
    print(res3)

    # chain()函数吧所有的输入参数连接成一个列表,然后返回每一个元素.如果参数的类型都相同,则可以通过使用加操作符吧集合连接起来达到同样的结果
    # 但是chain()也可以在不兼容加操作符的容器类型上工作
    items = it.chain([1, 2, 3], "astring", {"a", "set", "of", "strings"})
    for item in items:
        print(item)

    # 还有一个islice()函数.它的工作原理与切片操作符类似.由于它使用了生成器,因此在内存使用上更加高效.它与普通切片有一个很大的不同:你不能
    # 使用负索引值来从末端倒数,因为迭代器并非都有定义完善的缺点
    data = list(range(20))
    print(data[3:12:2])
    for d in it.islice(data, 3, 12, 2):
        print(d, end=" ")


def data_deal_function():
    # compress()函数像是位掩码的高级版本.它接受一个数据集合作为第一个参数,一个布尔值集合作为第二个参数.
    # 返回第一个集合中对应着第二个集合True值得那些项
    # 注意,布尔值并不是纯正的布尔值.它们可以是任何Python能转换成布尔值的东西,甚至是表达式
    # itertools.filterfalse()函数的工作原理完全相同,但是是相反的.它返回那些对应布尔值为False而不是True的元素
    for item in it.compress([1, 2, 3, 4, 5], [False, True, False, 0, 1]):
        print(item)

    # dropwhile()和takewhile()函数也有相关的单相反的效果.两个函数都接受一个输入函数和一个集合或迭代器作为参数,然后每次对输入数据元素应用函数.
    # dropwhile()函数会忽略所有输入元素直到函数参数返回结果为False.而takewhile()则返回元素直到结果为False
    # 注意,这两个函数在第一次检测到触发器之后都停止处理数据(一旦dropwhile停止丢掉,之后就不会丢掉任何东西了,而takewhile的接受行为是类似的)
    def __single_digit(n):
        return n < 10

    for n in it.dropwhile(__single_digit, range(20)):
        print(n, end=" ")
    for n in it.takewhile(__single_digit, range(20)):
        print(n, end=" ")

    # accumulate()函数把它的输入函数应用到输入数据的每个元素和之前操作的结果(默认函数是加,第一个结果总是第一个元素).因此,对于输入数据集
    # [1,2,3,4]来说,初始值result1是1.之后函数会被应用到result1和2产生result2,以此类推.最终结果值与应用functools模块的reduce()函数相同
    for n in it.accumulate([1, 2, 3, 4, ]):
        print(n, end=" ")


def test_groupby():
    data = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [0, 2, 4, 6, 8], [1, 3, 5, 7, 9]]
    for d in data:
        print(all(d))

    for ky, grp in it.groupby(data, key=all):
        print(ky, grp)
    # 可以看到groupby()返回了两个单独的组.它们的关键字都是True.为了避免它,必须在应用groupby()之前对数据进行排序
    for ky, grp in it.groupby(sorted(data, key=all), key=all):
        print(ky, grp)

    for ky, grp in it.groupby(sorted(data, key=all), key=all):
        if ky:
            trueset = grp
        else:
            falseset = grp
    for item in falseset:
        print(item)
    # falseset为空.这是因为falsesett组被最先创建,然后后面的迭代器grp继续前进.这使得刚刚存储在falseset中的值失效了.
    # 为了保存数据集方便后面处理,需要将它们存为列表
    groups = {True: [], False: []}
    for ky, grp in it.groupby(sorted(data, key=all), key=all):
        groups[ky].append(list(grp))
    print(groups)


def main():
    tools_function()
    data_deal_function()
    test_groupby()


if __name__ == "__main__":
    main()
