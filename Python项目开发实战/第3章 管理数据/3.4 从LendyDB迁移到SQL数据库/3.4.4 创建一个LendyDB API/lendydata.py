#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 专注于物品和成员的CRUD接口,需要使用之前的创建好数据库先.
查询函数都遵循同样的模式.一个SQL查询字符串被创建,使用三引号允许多行布局,然后这个字符串被传到cursor.execute()方法中.
取到的值在合适的地方被返回.自始至终一直使用cursor.execute()的参数替换机制.

两个更新方法都有默认的输入参数.这意味着用户可以只提供那些他们要改变的字段.其他字段的填充会基于使用适合的获得细节函数获取到的现有值
两个获得名称函数可以方便用户轻松地将从获得细节查询中返回的数据库标识符映射到有意义的名称.一般来说,应用程序员应该在向用户展示结果前使用这些函数

Lending library database API

Provides a CRUD interface to item and member entities and init an close functions for database control.
'''
__author__ = '__L1n__w@tch'

import sqlite3 as sql

db = None
cursor = None


##### CRUD functions for items ######
def insert_item(name, description, owner_id, price, condition):
    query = """insert into item (Name, Description, OwnerID, Price, Condition, DateRegistered) values (?,?,?,?,?,date('now'))"""
    cursor.execute(query, (name, description, owner_id, price, condition))


def get_items():
    query = """select ID, Name, Description, OwnerID, Price, Condition, DateRegistered from item"""
    return cursor.execute(query).fetchall()


def get_item_details(id):
    query = """select Name, Description, OwnerID, Price, Condition, DateRegistered from item where id = ?"""
    return cursor.execute(query, (id,)).fetchall()[0]


def get_item_name(id):
    return get_item_details(id)[0]


def update_item(id, name=None, description=None, owner_id=None, price=None, condition=None):
    query = """update item set Name=?,Description=?,OwnerID=?,Price=?,Condition=? where id=?"""
    data = get_item_details(id)
    if not name:
        name = data[0]
    if not description:
        description = data[1]
    if not owner_id:
        owner_id = data[2]
    if not price:
        price = data[3]
    if not condition:
        condition = data[4]
    cursor.execute(query, (name, description, owner_id, price, condition, id))


def delete_item(id):
    query = """delete from item where id=?"""
    cursor.execute(query, (id,))


##### CRUD functions for members ######
def insert_member(name, email):
    query = """insert into member (name,email) values (?,?)"""
    cursor.execute(query, (name, email))


def get_members():
    query = """select id, name, email from member"""
    return cursor.execute(query).fetchall()


def get_member_details(id):
    query = """select name, email from member where id = ?"""
    return cursor.execute(query, (id,)).fetchall()[0]


def get_member_name(id):
    return get_member_details(id)[0]


def update_member(id, name=None, email=None):
    query = """update member set name=?, email=? where id=?"""
    data = get_member_details(id)
    if not name:
        name = data[0]
    if not email:
        email = data[1]
    cursor.execute(query, (name, email, id))


def delete_member(id):
    query = """delete from member where id=?"""
    cursor.execute(query, (id,))


##### Databae init and close ######
def init_db(file_name=None):
    global db, cursor
    if not file_name:
        file_name = "lendy.db"
    try:
        db = sql.connect(file_name)
        cursor = db.cursor()
    except:
        print("Error connecting to", file_name)
        cursor = None
        raise


def close_db():
    try:
        cursor.close()
        db.commit()
        db.close()
    except:
        print("problem closing database...")
        raise


def test_api():
    init_db()
    print(get_members())
    print(get_items())

    # 以下证明完整性检查正常工作
    try:
        insert_item("Python Projects", "Book", 6, 30, "Excellent")
    except Exception as e:
        print(e)

    insert_member("Alan", "alan@emailaddress.com")
    print(get_members())
    insert_item("Python Projects", "Book", 6, 30, "Excellent")
    print(get_items())

    update_item(7, price=25)
    print(get_item_details(7))
    print(get_member_name(6))
    update_member(6, name="Alan Gauld")
    print(get_member_details(6))

    try:
        delete_member(6)
    except Exception as e:
        print(e)
    delete_item(7)
    delete_member(6)

    print(cursor.execute(
            """select * from item where OwnerID in (select id from member where name like '%e%')""").fetchall())
    print(cursor.execute(
            """select * from item where OwnerID not in (select id from member where name like '%e%')""").fetchall())
    print(get_member_name(4))

    close_db()


def main():
    init_db()  # use default file

    print("Members:\n", get_members())
    print("Items:\n", get_items())
    close_db()

    test_api()


if __name__ == "__main__":
    main()
