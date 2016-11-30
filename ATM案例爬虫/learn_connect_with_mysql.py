#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.11.30 学习如何跟 MySQL 交互的
"""
import pymysql

__author__ = '__L1n__w@tch'


def create_tables(cursor):
    """
    负责创建表格的
    :param cursor: 游标
    :return:
    """
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS t_atm_cases_data")

    # 使用预处理语句创建表
    sql = ("""CREATE TABLE t_atm_cases_data (
           case_id CHAR(24) NOT NULL,
           case_path TEXT NOT NULL,
           case_content TEXT,
           PRIMARY KEY (case_id) )"""
           )

    cursor.execute(sql)


def insert_data_to_tables(cursor, db):
    """
    往表中插入数据
    :param cursor: 游标
    :param db: 数据库
    :return:
    """
    # SQL 插入语句
    sql1 = r"INSERT INTO t_atm_cases_data(case_id, case_path, case_content)" \
           r"VALUES ('57eb3d9ed10540526e001170', 'asdads', '#大家好')"

    sql2 = r"INSERT INTO t_atm_cases_data(case_id, case_path, case_content)" \
           r"VALUES ('57eb3d9ed10540526e001172', '22222', '#大家好222')"

    try:
        # 执行sql语句
        cursor.execute(sql1)
        cursor.execute(sql2)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()
        raise e


def query_data_from_tables(cursor):
    """
    从表中查询数据
    # 可以使用 fetchone() 方法获取单条数据.db_cursor.fetchone()
    :param cursor: 游标
    :return:
    """
    # SQL 查询语句
    sql = "SELECT * FROM t_atm_cases_data"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print(results)
    except Exception as e:
        print("获取数据失败")
        raise e


if __name__ == "__main__":
    # 打开数据库连接
    my_db = pymysql.connect(host="localhost", user="root", passwd="root", db="TESTDB", charset="utf8")

    # 使用 cursor() 方法创建一个游标对象 cursor
    db_cursor = my_db.cursor()

    # 创建表格
    create_tables(db_cursor)

    # 插入数据
    insert_data_to_tables(db_cursor, my_db)

    # 查询数据
    query_data_from_tables(db_cursor)

    # 关闭数据库连接
    my_db.close()
