#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 使用itertools函数来重复之前LendyDB数据的分析.
'''
__author__ = '__L1n__w@tch'

import itertools

items = [
    ['ID', 'Name', 'Description', 'OwnerID', 'Price', 'Condition', 'Registered'],
    ['1', 'Lawnmower', 'Tool', '1', '$150', 'Excellent', '2012-01-05'],
    ['2', 'Lawnmower', 'Tool', '2', '$370', 'Fair', '2012-04-01'],
    ['3', 'Bike', 'Vehicle', '3', '$200', 'Good', '2013-03-22'],
    ['4', 'Drill', 'Tool', '4', '$100', 'Good', '2013-10-28'],
    ['5', 'Scarifier', 'Tool', '5', '$200', 'Average', '2013-09-14'],
    ['6', 'Sprinkler', 'Tool', '1', '$80', 'Good', '2014-01-06']
]

members = [
    ['ID', 'Name', 'Email'],
    ['1', 'Fred', 'fred@lendylib.org'],
    ['2', 'Mike', 'mike@gmail.com'],
    ['3', 'Joe', 'joe@joesmail.com'],
    ['4', 'Rob', 'rjb@somcorp.com'],
    ['5', 'Anne', 'annie@bigbiz.com'],
]

loans = [
    ['ID', 'ItemID', 'BorrowerID', 'DateBorrowed', 'DateReturned'],
    ['1', '1', '3', '4/1/2012', '4/26/2012'],
    ['2', '2', '5', '9/5/2012', '1/5/2013'],
    ['3', '3', '4', '7/3/2013', '7/22/2013'],
    ['4', '4', '1', '11/19/2013', '11/29/2013'],
    ['5', '5', '2', '12/5/2013', 'None']
]


def cost(item):
    return int(item[4][1:])


def owner(item):
    return item[3]


def returned(loan):
    return not (loan[-1] == "None")


def main():
    # 所有物品的总成本是多少?
    # 使用accumulate()函数产生了连续的成本计数,然后使用islice()并指定一个开始索引len(items)-2和结束索引None来只抽取最后一项
    for n in itertools.islice(itertools.accumulate(cost(item) for item in items[1:]), len(items) - 2, None):
        print(n)

    # 单个物品的平均成本是多少?
    print(n / (len(items) - 1))

    # 谁贡献的物品最多?
    owners = {}
    for ky, grp in itertools.groupby(sorted(items[1:], key=owner), key=owner):
        owners[ky] = len(list(grp))
    for member in members[1:]:
        print(member[1], " : ", owners[member[0]])

    # 反转辅助函数returned()的逻辑,让它返回一个物品是否已经被返回.通过在filterfalse()函数中使用它,可以发现那些还没有被返回的物品,也就是处于借出状态的物品
    print([items[int(loan[1])] for loan in itertools.filterfalse(returned, loans)])


if __name__ == "__main__":
    main()
