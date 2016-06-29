#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 平时自己做计划的格式类似如下:

2016.06.29 周三:
    早上:
        08:10~09:10:	Python 整理
        09:10~10:10:	考试安排 + 微机原理

    下午:
        13:30~14:30:
        14:30~15:30:
        15:30~16:30:
        16:30~17:30:

    晚上:
        18:30~19:30:
        19:30~20:30:
        20:30~21:30:

唯一的问题是每次都要手敲, 所以还是程序解决吧
"""
import datetime
import calendar

__author__ = '__L1n__w@tch'


def is_leap_year(year, learn=True):
    """
    判断是不是闰年
    :param year: 2004
    :param learn: 看是要自己算还是调用库函数
    :return: True
    """
    if learn:
        return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)
    else:
        return calendar.isleap(year)


def create_date(start_date=datetime.date.today(), number=15):
    """
    实现效果, 产生如下的字符串
        '''
        2016.06.29 周三:
        2016.06.30 周四:
        2016.07.01 周五:
        2016.07.02 周六:
        '''
    :param start_date: 从哪个日期开始产生, 格式为 (2016,7,9,5), 表示 year=2016, month=7, day=9, week_day=5
    :param number: 要产生多少个字符串
    :return: None
    """
    week_days = ["一", "二", "三", "四", "五", "六", "日"]
    date = start_date

    for i in range(number):
        year, month, day, week_day = date.year, date.month, date.day, date.weekday()
        string = "{}.{}.{} 周{}:".format(year, str(month).zfill(2), str(day).zfill(2), week_days[week_day % 7])
        print(string)

        # 更新下一天
        date += datetime.timedelta(days=1)


if __name__ == "__main__":
    create_date()
