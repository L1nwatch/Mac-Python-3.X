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
    in_url = peewee.TextField()
    out_url = peewee.TextField()


class ID2URL(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase(database_name)

    page_id = peewee.CharField(unique=True, null=True)
    page_url = peewee.TextField(null=True)


def create_database():
    """
    负责创建 sqlite3 数据库, 如果已存在则进行连接操作
    :return: sqlite3 的 db 实例
    """
    db = sqlite3.connect(database_name)
    return db


def read_file_data(file_name):
    """
    读取文件中的每一行, 按空格间隔后返回
    :param file_name: str(), 比如 "link_relationship.txt"
    :return: tuple, (str(), str()), 比如 ("1", "https://1.html")
    """
    with open(file_name, "r") as f:
        for each_line in f:
            yield each_line.split("\t")


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
    for each_id, each_url in read_file_data(file_path):
        each_row = ID2URL(page_id=each_id, page_url=each_url)
        each_row.save()

    # 创建 LinkRelationship 数据
    file_path = os.path.join("/Users/L1n/Desktop/Notes/毕设/毕设实现/工程文件/SogouT-Link.v1", "SogouT-link")
    print("[*] 读取文件 {} 并插入数据库".format(str(file_path).rsplit("/", maxsplit=1)[1]))
    for each_id, each_in, each_out in read_file_data(file_path):
        link_relation_ship = LinkRelationShip(page_id=each_id, in_url=each_in, out_url=each_out)
        link_relation_ship.save()


def run():
    # 创建数据库
    db = create_database()

    # 创建链接数据
    create_link_relationship_db(db, "link_relationship.txt")

    # 访问数据库, 验证是否插入成功
    print("[*] 尝试访问数据库")
    assert len(LinkRelationShip.select()) > 1
    assert len(ID2URL.select()) > 1
    print("[*] 成功插入数据到数据库中")


if __name__ == "__main__":
    run()
