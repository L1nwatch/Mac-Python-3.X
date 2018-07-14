#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 微信聊天记录导出

要求先得到 MM.sqlite 文件
"""
import peewee

db = peewee.SqliteDatabase("MM.sqlite")

__author__ = '__L1n__w@tch'


def main():
    possible_table = list()

    # 只找指定日期 xxx 之前的
    for each_table in db.get_tables():
        if each_table.startswith("Chat_"):
            found = False
            result = db.execute_sql("select * from {}".format(each_table))
            for each_result in result:
                message = each_result[3]

                if int(message) >= 1515861737 or int(message) <= 1511827168:
                    found = False
                    break
                else:
                    found = True
            if found:
                possible_table.append(each_table)

    # 只找里面包含 xxx 的
    print(possible_table)
    for each_possible_table in possible_table:
        if each_possible_table in ("Chat_04d5f83ad9fec6edd398bbab8bccff3d", "Chat_1298a62b80eae006d901074c0f146a38",
                                   "Chat_14c889445866b8c1207a0d60629fe2af", "Chat_16449357365a042cf0b88452731ee69a",
                                   "Chat_2c72460f68202af22189e72dac9dd140", "Chat_40606ccc952c2602aa80bd2c071f3683",
                                   "Chat_42de604cf28318c8226014ce829ff78e", "Chat_52842833ef4d7b638069a3a43af16e78",
                                   "Chat_52b09bfb81b97f5416f563a387058933", "Chat_59722f70ca275022e1c6fcdbd36143cd",
                                   "Chat_6df0e0eea400de81e8c3e488575e789b", "Chat_74afaf5c470e93a6c3c2c50046c1e7ba",
                                   "Chat_8ce7fa56ea2537d449377b477b9f4c86"):
            continue

        result = db.execute_sql("select * from {}".format(each_possible_table))
        type_count = 0
        found = True
        for i, each_result in enumerate(result):
            message_type = each_result[7]
            if message_type == 49:
                type_count += 1
            if i >= 4 and type_count >= 3:
                found = False
                break
        if found and i >= 4:
            print(each_possible_table)


if __name__ == "__main__":
    main()
