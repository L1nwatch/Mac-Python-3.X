#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 代码将把工具借出电子表格中的数据转换为LendyDB的数据格式,并把它保存为三组DBM文件.
然后,通过读取文件并打印内容,你将证实它可以正确工作
Windows Only, 在Mac下运行不成功
'''
__author__ = '__L1n__w@tch'

import dbm  # 导入了dbm模块(模块在内部分析你的系统,决定哪个DBM库是可用的并把它初始化以供使用)

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


def create_db(data, db_name):
    try:
        db = dbm.open(db_name, "c")  # c代表创建模式,如果文件不存在,c模式会创建一个新文件.如果已存在,它会打开这个文件
        for datum in data:
            db[datum[0]] = ",".join(datum)  # 使用第一个字段作为主键,然后把所有字段连接成逗号分隔的字符串
    finally:
        db.close()
        print(db_name, "created")


def read_db(db_name):
    """
    读取模式打开了文件,然后返回了用列表推导产生的一个列表
    :param db_name:
    :return:
    """
    try:
        db = dbm.open(db_name, "r")
        print("Reading ", db_name)
        return [db[datum] for datum in db]
    finally:
        db.close()


def test_edit_db():
    items = dbm.open("itemdb")
    members = dbm.open("memberdb")
    loans = dbm.open("loandb", "w")
    loan2 = loans["2"].decode()
    print(loan2)
    loan2 = loan2.split(",")
    print(loan2)
    item2 = items[loan2[1]].decode().split(",")
    print(item2)
    member2 = members[loan2[2]].decode().split(",")
    print(member2)
    print("{} borrowed a {} on {}".format(member2[1], item2[1], loan2[3]))

    print(max(loans.keys()).decode())  # 使用max()函数在loans数据库中查找已存键的最高值
    key = int(max(loans.keys()).decode()) + 1
    newloan = [str(key), "2", "1", "4/5/2014"]
    loans[str(key)] = ",".join(newloan) # 创建新建
    print(loans[str(key)])


def main():
    print("Creating data files...")
    # 注意,你并没有提供任何文件扩展名,dbm自己做了这件事
    # dbm创建的数据库包含三个文件,一个文件保存了实际数据,其他两个文件保存着dbm用来查找数据文件中记录的索引信息
    # 就是这个索引机制让dbm远远快于在纯文本文件钟的简单顺序搜索.你不应该直接编辑dbm文件,这可能损坏你的数据库
    create_db(items, "itemdb")
    create_db(members, "memberdb")
    create_db(loans, "loandb")

    # r模式用来只读访问已存在的数据库、w用来读取或写入已存在的数据库、c创建新数据库或打开已存在的数据库、n永远会创建一个新的空数据库
    print("reading data files...")
    print(read_db("itemdb"))
    print(read_db("memberdb"))
    print(read_db("loandb"))

    test_edit_db()


if __name__ == "__main__":
    main()
