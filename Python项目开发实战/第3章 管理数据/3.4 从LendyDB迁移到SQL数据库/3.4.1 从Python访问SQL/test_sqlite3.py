#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' sqlite3库的示例代码,在Mac下运行通过
'''
__author__ = '__L1n__w@tch'

import sqlite3


def find_data(cursor, a_string):
    cursor.execute("select * from test where name like ?", (a_string,))
    return cursor.fetchall()


def main():
    # db = sqlite3.connect(
    #         r"/Users/L1n/Desktop/Python Projects/PyCharm/Python项目开发实战/第3章 管理数据/3.4 从LendyDB迁移到SQL数据库/3.4.1 从Python访问SQL/lendy.db")
    # :memory:表示想要一个存在计算机内存中的临时数据库
    db = sqlite3.connect(":memory:")
    cur = db.cursor()
    cur.execute("create table test(id, name)")
    cur.execute("insert into test (id,name) values (1, 'Alan')")
    cur.execute("insert into test (id,name) values (2, 'Laura')")
    cur.execute("insert into test (id,name) values (3, 'Jennifer')")
    cur.execute("Select * FROM test")
    # 使用游标的fetchall()方法查看元组的列表输出(其他选项包括在循环内部使用 fetchone()或用fetchmany()返回一批结果)
    print(cur.fetchall())

    print(find_data(cur, "A%"))
    print(find_data(cur, "%a%"))

    cur.execute("delete from test")
    cur.execute("drop table test")
    cur.close()
    # DBAPI有时会调用commit,而有时候需要显式地做这件事.一般情况下,应该总是在关闭数据库连接前调用commit.
    # 在示例中数据库只存在于内存中并且会在你关闭连接时消失.如果在使用一个基于文件的数据库,则需要commit()来确保你所做改变在下次打开数据库时可见
    db.commit()  # 执行了连接的commit()方法,它会永久地应用产生的改变
    db.close()


if __name__ == "__main__":
    main()
