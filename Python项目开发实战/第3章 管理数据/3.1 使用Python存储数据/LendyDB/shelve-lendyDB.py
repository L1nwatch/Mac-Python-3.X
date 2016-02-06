#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 使用shelve重复了dbm示例中的功能.
'''
__author__ = '__L1n__w@tch'

import shelve

# ID, Name, Description, OwnerID, Price, Condition, DateRegistered
items = [
    ['1', 'Lawnmower', 'Tool', '1', '$150', 'Excellent', '2012-01-05'],
    ['2', 'Lawnmower', 'Tool', '2', '$370', 'Fair', '2012-04-01'],
    ['3', 'Bike', 'Vehicle', '3', '$200', 'Good', '2013-03-22'],
    ['4', 'Drill', 'Tool', '4', '$100', 'Good', '2013-10-28'],
    ['5', 'Scarifier', 'Tool', '5', '$200', 'Average', '2013-09-14'],
    ['6', 'Sprinkler', 'Tool', '1', '$80', 'Good', '2014-01-06']
]

# ID, Name, Email
members = [
    ['1', 'Fred', 'fred@lendylib.org'],
    ['2', 'Mike', 'mike@gmail.com'],
    ['3', 'Joe', 'joe@joesmail.com'],
    ['4', 'Rob', 'rjb@somcorp.com'],
    ['5', 'Anne', 'annie@bigbiz.com'],
]

# ID, ItemID, BorrowerID, DateBorrowed, DateReturned
loans = [
    ['1', '1', '3', '4/1/2012', '4/26/2012'],
    ['2', '2', '5', '9/5/2012', '1/5/2013'],
    ['3', '3', '4', '7/3/2013', '7/22/2013'],
    ['4', '4', '1', '11/19/2013', '11/29/2013'],
    ['5', '5', '2', '12/5/2013', 'None']
]


def create_db(data, shelf_name):
    try:
        shelf = shelve.open(shelf_name, "c")
        # 相比于dbm, 这里不需要join()方法处理数据就可以直接写入
        for datum in data:
            shelf[datum[0]] = datum
    finally:
        shelf.close()


def read_db(shelf_name):
    try:
        shelf = shelve.open(shelf_name, "r")
        return [shelf[key] for key in shelf]
    finally:
        shelf.close()


def test():
    """
    相比于dbm,不需要再进行split()操作来获得一个列表,并且不需要使用decode()把字节转换成普通字符串
    :return:
    """
    items = shelve.open("itemshelf", "w")
    members = shelve.open("membershelf", "w")
    loans = shelve.open("loanshelf", "w")
    loan2 = loans["2"]
    print(loan2)

    item2 = items[loan2[1]]
    print(item2)
    member2 = members[loan2[2]]
    print("{} borrowed a {} on {}".format(member2[1], item2[1], loan2[3]))

    key = int(max(loans.keys())) + 1
    newloan = [str(key), "2", "1", "4/5/2014"]
    loans[str(key)] = newloan
    print(loans[str(key)])
    loans.close()  # make the change permanent


def main():
    print("Creating data files...")
    create_db(items, "itemshelf")
    create_db(members, "membershelf")
    create_db(loans, "loanshelf")

    print("reading items...")
    print(read_db("itemshelf"))
    print("reading members...")
    print(read_db("membershelf"))
    print("reading loans...")
    print(read_db("loanshelf"))

    test()


if __name__ == "__main__":
    main()
