#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import sqlite3

members = [
    ['Fred', 'fred@lendylib.org'],
    ['Mike', 'mike@gmail.com'],
    ['Joe', 'joe@joesmail.com'],
    ['Rob', 'rjb@somcorp.com'],
    ['Anne', 'annie@bigbiz.com'],
]
member_sql = '''insert into member (Name, Email) values (?, ?)'''

items = [
    ['Lawnmower', 'Tool', 0, 150, 'Excellent', '2012-01-05'],
    ['Lawnmower', 'Tool', 0, 370, 'Fair', '2012-04-01'],
    ['Bike', 'Vehicle', 0, 200, 'Good', '2013-03-22'],
    ['Drill', 'Tool', 0, 100, 'Good', '2013-10-28'],
    ['Scarifier', 'Tool', 0, 200, 'Average', '2013-09-14'],
    ['Sprinkler', 'Tool', 0, 80, 'Good', '2014-01-06']
]
# 日期格式!尽管SQLite没有Date数据类型,但是它有一些可以用来创建标准日期字符串和值的函数.然后SQLite把它们保存为文本(或者在一些情况下存储为浮点数)
# 这里使用的date()函数要求日期字符串是所示的格式,而一个非法日期字符串会被存储为NULL.因此,通过确保只有有效的、格式一致的日期被存储,使用date()改善了数据质量
item_sql = '''insert into item (Name, Description, ownerID, Price, Condition, DateRegistered) values (?, ?, ?, ?, ?, date(?))'''
set_owner_sql = '''
update item
set OwnerID = (SELECT ID from member where name = ?)
where item.id = ?
'''

loans = [
    [1, 3, '2012-01-04', '2012-04-26'],
    [2, 5, '2012-09-05', '2013-01-05'],
    [3, 4, '2013-07-03', '2013-07-22'],
    [4, 1, '2013-11-19', '2013-11-29'],
    [5, 2, '2013-12-05', None]
]
loan_sql = '''insert into loan (itemID, BorrowerID, DateBorrowed, DateReturned ) values (?, ?, date(?), date(?))'''


def main():
    db = sqlite3.connect("test.db")
    cur = db.cursor()

    cur.executemany(member_sql, members)
    cur.executemany(item_sql, items)
    cur.executemany(loan_sql, loans)

    owners = ("Fred", "Mike", "Joe", "Rob", "Anne", "Fred")
    for item in cur.execute("select id from item").fetchall():
        itemID = item[0]
    cur.execute(set_owner_sql, (owners[itemID - 1], itemID))

    cur.close()
    db.commit()
    db.close()


if __name__ == "__main__":
    main()
