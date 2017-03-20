#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 负责新建 sqlite3 数据库, 以及插入对应的链接关系库, 以便毕设进行查询访问等操作

2017.03.20 实现新建 sqlite3 数据库以及伪造部分链接关系数据, 另外顺便学习一下 peewee
"""
import sqlite3
import peewee
import os

__author__ = '__L1n__w@tch'

database_name = "link_relationship.db"


class LinkRelationShip(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase(database_name)

    page_id = peewee.CharField()
    out_id = peewee.CharField()


class ID2URL(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase(database_name)

    page_id = peewee.CharField(null=True)
    page_url = peewee.TextField(null=True)


def create_database():
    """
    负责创建 sqlite3 数据库, 如果已存在则进行连接操作
    :return: sqlite3 的 db 实例
    """
    db = sqlite3.connect(database_name)
    return db


def read_file_data(file_name, field_name):
    """
    读取文件中的每一行, 按空格间隔后返回
    每次读取 1w 行
    :param file_name: str(), 比如 "link_relationship.txt"
    :param field_name: 从文件里读取的每一列的含义
    :return: tuple, (str(), str()), 比如 ("1", "https://1.html")
    """
    with open(file_name, "r") as f:
        counts = 0
        temp_list = list()
        for each_line in f:
            counts += 1
            temp_list.append({key: value.strip() for key, value in zip(field_name, each_line.split("\t"))})
            if counts == 400:
                yield temp_list
                del temp_list[:]
                counts = 0
                # temp_list.clear() # python3.2 居然没有这个方法


def clear_database():
    print("[*] 执行清除数据库操作")
    # 确保表和库存在, 之后清除数据后重建表
    if LinkRelationShip.table_exists() and ID2URL.table_exists():
        # 清除原来的数据
        LinkRelationShip.drop_table()
        LinkRelationShip.create_table()

        ID2URL.drop_table()
        ID2URL.create_table()


def create_link_relationship_db(database, file_path):
    """
    负责创建链接数据库相关的表, 插入或更新数据等操作
    :param database: sqlite3 的 db 实例
    :param file_path: str(), 链接数据的文件, 比如 "link_relationship.txt"
    :return: None
    """
    # 确保表和库存在
    clear_database()
    LinkRelationShip.create_table() if not LinkRelationShip.table_exists() else None
    ID2URL.create_table() if not ID2URL.table_exists() else None

    # 创建 ID2URL 的数据
    file_path = os.path.join("/Users/L1n/Desktop/Notes/毕设/毕设实现/工程文件/SogouT-Link.v1", "id2url.link")
    print("[*] 读取文件 {} 并插入数据库".format(str(file_path).rsplit("/", maxsplit=1)[1]))
    for data_source_list in read_file_data(file_path, ["page_id", "page_url"]):
        ID2URL.insert_many(data_source_list).execute()

    # 创建 LinkRelationship 数据
    file_path = os.path.join("/Users/L1n/Desktop/Notes/毕设/毕设实现/工程文件/SogouT-Link.v1", "SogouT-link")
    print("[*] 读取文件 {} 并插入数据库".format(str(file_path).rsplit("/", maxsplit=1)[1]))
    for data_source_list in read_file_data(file_path, ["page_id", "out_id"]):
        LinkRelationShip.insert_many(data_source_list).execute()


def run():
    # 创建数据库
    db = create_database()

    # 创建链接数据
    confirm = input("[+] 即将修改数据库中的数据, 确认?[y/n]")
    if confirm.lower() == "y":
        create_link_relationship_db(db, "link_relationship.txt")

    # 访问数据库, 验证是否插入成功
    print("[*] 尝试访问数据库")
    assert len(LinkRelationShip.select().limit(10)) > 1
    assert len(ID2URL.select().limit(10)) > 1
    print("[*] 成功插入数据到数据库中")


if __name__ == "__main__":
    run()
