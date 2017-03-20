#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 负责新建 sqlite3 数据库, 以及插入对应的链接关系库, 以便毕设进行查询访问等操作

2017.03.20 发现数据源里面好多链接冗余, 于是特殊处理一下
2017.03.20 实现新建 sqlite3 数据库以及伪造部分链接关系数据, 另外顺便学习一下 peewee
"""
import sqlite3
import peewee
import os
import timeit

from xml2json import get_docs_from_file, parse_doc_to_dict

__author__ = '__L1n__w@tch'

database_name = "link_relationship.db"


class LinkRelationShip(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase(database_name)

    page_id = peewee.CharField()
    out_id = peewee.CharField()


class PageID2URL(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase(database_name)

    page_id = peewee.CharField(null=False)
    page_url = peewee.TextField(null=False)


class DomainID2URL(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase(database_name)

    page_id = peewee.CharField(null=False)
    page_url = peewee.TextField(null=False)


class LinkInDoc(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase(database_name)

    domain_id = peewee.CharField(null=False)
    out_id = peewee.CharField(null=True)
    in_id = peewee.CharField(null=True)


def create_database():
    """
    负责创建 sqlite3 数据库, 如果已存在则进行连接操作
    :return: sqlite3 的 db 实例
    """
    db = sqlite3.connect(database_name)
    return db


def special_deal(data, choice=1):
    """
    主要针对表 LinkRelationShip, 只保留域名到域名的指向关系
    :param data: str(), 需要处理的数据, 比如 "6a4c0d0f7adf1d20-6ef9b1edc1c18510	6a4c0d0f7adf1d20-6ef9b1edc1c18510"
    :param choice: int(), 表明是什么特殊处理方法
    :return: str(), 处理过后的数据, 比如 "6ef9b1edc1c18510\t6ef9b1edc1c18510"
    """
    if choice == 1:
        # 表明是 LinkRelationShip 的特殊处理
        source, destination = data.split("\t")
        source, destination = source.split("-")[1], destination.split("-")[1]
    else:
        # 表明是 DomainID2URL 的特殊处理
        source, destination = data.split("\t")
        source = source.split("-")[1]
    return "{}\t{}".format(source, destination)


def read_file_data(file_name, field_name, need_special_deal=0):
    """
    读取文件中的每一行, 按空格间隔后返回
    每次读取 1w 行
    :param file_name: str(), 比如 "link_relationship.txt"
    :param field_name: 从文件里读取的每一列的含义
    :param need_special_deal: int(), 区分一下是否需要特殊处理, 0 表示不用特殊处理
    :return: tuple, (str(), str()), 比如 ("1", "https://1.html")
    """
    with open(file_name, "r") as f:
        counts = 0
        temp_list = list()
        for each_line in f:
            counts += 1
            if need_special_deal != 0:
                each_line = special_deal(each_line, need_special_deal)
            temp_list.append({key: value.strip() for key, value in zip(field_name, each_line.split("\t"))})
            if counts == 400:
                yield temp_list
                del temp_list[:]
                counts = 0
                # temp_list.clear() # python3.2 居然没有这个方法


def clear_database(tables):
    """
    清除指定表
    :param tables: list(), 每个是表的类, 比如 []
    :return: None
    """
    print("[*] 执行清除数据库操作")
    # 确保表和库存在, 之后清除数据后重建表
    for each_table in tables:
        if each_table.table_exists():
            # 清除原来的数据
            each_table.drop_table()
            each_table.create_table()
        else:
            each_table.create_table()


def create_link_relationship_db(database, file_path):
    """
    负责创建链接数据库相关的表, 插入或更新数据等操作
    :param database: sqlite3 的 db 实例
    :param file_path: str(), 链接数据的文件, 比如 "link_relationship.txt"
    :return: None
    """
    # 确保表和库存在, 且为初始状态
    clear_database([LinkRelationShip, PageID2URL, DomainID2URL])

    # 创建 ID2URL 的数据
    file_path = os.path.join("/Users/L1n/Desktop/Notes/毕设/毕设实现/工程文件/SogouT-Link.v1", "id2url.link")
    print("[*] 读取文件 {} 并插入表 PageID2URL".format(str(file_path).rsplit("/", maxsplit=1)[1]))
    for data_source_list in read_file_data(file_path, ["page_id", "page_url"]):
        PageID2URL.insert_many(data_source_list).execute()

    print("[*] 读取文件 {} 并插入表 DomainID2URL".format(str(file_path).rsplit("/", maxsplit=1)[1]))
    for data_source_list in read_file_data(file_path, ["page_id", "page_url"], need_special_deal=2):
        DomainID2URL.insert_many(data_source_list).execute()

    # 创建 LinkRelationship 数据
    file_path = os.path.join("/Users/L1n/Desktop/Notes/毕设/毕设实现/工程文件/SogouT-Link.v1", "SogouT-link")
    print("[*] 读取文件 {} 并插入数据库".format(str(file_path).rsplit("/", maxsplit=1)[1]))
    for data_source_list in read_file_data(file_path, ["page_id", "out_id"], need_special_deal=1):
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
    assert len(DomainID2URL.select().limit(10)) > 1
    print("[*] 成功插入数据到数据库中")


def compare_db_data():
    """
    将搜狗数据源的新闻数据与数据库中的数据相比较, 看有多少条匹配的信息在里头
    另外将比较的结果保存在表 LinkInDoc 里面
    结果是只有 6 个域名有匹配信息, 280 个域名没有匹配信息
    :return:
    """
    file_path = os.path.join("/Users/L1n/Desktop/Code/Python/PyCharm/毕设辅助脚本/xml转json", "news_tensite_xml.dat")
    domain_dict = dict()
    if not LinkInDoc.table_exists():
        LinkInDoc.create_table()
    else:
        LinkInDoc.drop_table()
        LinkInDoc.create_table()

    for i, each_doc in enumerate(get_docs_from_file(file_path)):
        doc_dict = parse_doc_to_dict(each_doc)
        domain_id = doc_dict["doc_number"].split("-")[1]
        if domain_id in domain_dict:
            continue

        result = LinkRelationShip.select().where(
            LinkRelationShip.page_id == domain_id or LinkRelationShip.out_id == domain_id
        ).execute()
        if result.count > 0:
            domain_dict[domain_id] = True
            print("[*] {} 找到了!目前是第 {} 个文档, 总共 1294233 个文档".format(domain_id, i + 1))
            for each_row in result:
                # 如果是该网页被其他网页指向
                if each_row.out_id == domain_id:
                    LinkInDoc.insert({"domain_id": domain_id, "in_id": each_row.page_id}).execute()
                # 如果是该网页指向其他网页
                elif each_row.page_id == domain_id:
                    LinkInDoc.insert({"domain_id": domain_id, "out_id": each_row.out_id}).execute()
        else:
            domain_dict[domain_id] = False
            print("[-] {} 找不到!目前是第 {} 个文档, 总共 1294233 个文档".format(domain_id, i + 1))

    print("[*] 总共有域名 {} 个".format(len(domain_dict)))
    count_true, count_false = 0, 0
    for key, value in domain_dict.items():
        if value:
            count_true += 1
        else:
            count_false += 1
    print("[*] 有效域名: {} 个, 无效域名: {} 个".format(count_true, count_false))


def first_way_to_check():
    try:
        LinkRelationShip.get(page_id="69713306c0bb3300")
        LinkRelationShip.get(page_id="49f37189a1acd500")
    except peewee.DoesNotExist:
        pass


def second_way_to_check():
    test_1 = LinkRelationShip.select().where(LinkRelationShip.page_id == "69713306c0bb3300").execute()
    test_2 = LinkRelationShip.select().where(LinkRelationShip.page_id == "49f37189a1acd500").execute()

    for each in test_1:
        print(each.page_id)
        print(each.out_id)


if __name__ == "__main__":
    run()
    compare_db_data()

    # 比较那个快一些
    # print(timeit.timeit("first_way_to_check()", "from __main__ import first_way_to_check", number=200))
    # print(timeit.timeit("second_way_to_check()", "from __main__ import second_way_to_check", number=200))
    pass
