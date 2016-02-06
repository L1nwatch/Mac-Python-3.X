#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 以下使用标准Python特性来进行相关数据分析操作
'''
__author__ = '__L1n__w@tch'

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


def on_loan(loan):
    return loan[-1] == "None"


def main():
    print(cost(items[2]))
    print(sum(cost(item) for item in items[1:]))

    print(sum(cost(item) for item in items[1:]) / (len(items) - 1))

    for member in members[1:]:
        count = 0
        for item in items[1:]:
            if owner(item) == member[0]:
                count += 1
        print(member[1], ":", count)

    print([items[int(loan[1])] for loan in loans if on_loan(loan)])


if __name__ == "__main__":
    main()
