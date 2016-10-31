#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 平时自己做计划的格式类似如下:

2016.07.21 周四:
    早上:
        08:05~09:05:   GitHub 整理
        09:05~10:05:   Python 学习
        10:05~11:05:   尚未安排
        11:05~11:30:   尚未安排
    下午:
        13:31~14:31:   GitHub 整理
        14:31~15:31:   Python 学习
        15:31~16:31:   尚未安排
        16:31~17:30:   尚未安排
    晚上:
        18:59~19:59:   GitHub 整理
        19:59~20:59:   Python 学习
        20:59~21:30:   尚未安排

唯一的问题是每次都要手敲, 所以还是程序解决吧, 最终结果就是如上图所示
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


def create_format_hour_plan(start_hour="08:10", end_hour="10:10", things_list=None, step_seconds=3600):
    """
    创建格式化的时间表, 生成的形式类似于下面的:
        08:10~09:10:	Python 整理
        09:10~10:10:	考试安排 + 微机原理
    :param step_seconds: 时间段单元, 即每隔多少秒安排下一个计划
    :param start_hour: "08:10"
    :param end_hour: "10:10"
    :param things_list: ["Python 整理", "考试安排 + 微机原理"]
    :return: ['08:10~09:10:   尚未安排', '09:10~10:10:   尚未安排']
        '''
        08:10~09:10:	Python 整理
        09:10~10:10:	考试安排 + 微机原理
        '''
    """
    hour_plan_list = list()

    def __get_time_list(start, end, split_time):
        """
        给定一个开始时间和结束时间, 产生一个时间列表
        :param start: 开始时间, 比如 "08:10"
        :param end: 结束时间, 比如 "09:10"
        :param split_time: 每隔多少秒生成下一个时间段
        :return: ["08:10~09:10", "09:10~10:10"]
        """
        a_list = list()

        # 相关初始化
        today = datetime.datetime.today()
        year, month, day = today.year, today.month, today.day
        int_start_hour, int_start_minute = [int(_) for _ in start.split(":")]
        int_end_hour, int_end_minute = [int(_) for _ in end.split(":")]

        # 产生如下的东西: 2016-07-21 08:10:00
        start_date = datetime.datetime(year, month, day, int_start_hour, int_start_minute)
        # 产生如下的东西: 2016-07-21 10:10:00
        end_date = datetime.datetime(year, month, day, int_end_hour, int_end_minute)

        # 生成各个时间段
        while start_date < end_date:
            next_time = start_date + datetime.timedelta(seconds=split_time)
            result = "{}:{}~".format(str(start_date.hour).zfill(2), str(start_date.minute).zfill(2))
            if next_time <= end_date:
                a_list.append(result + "{}:{}".format(str(next_time.hour).zfill(2), str(next_time.minute).zfill(2)))
            else:
                a_list.append(result + "{}:{}".format(str(end_date.hour).zfill(2), str(end_date.minute).zfill(2)))
            start_date = next_time
        return a_list

    time_list = __get_time_list(start_hour, end_hour, step_seconds)

    if things_list is None:
        things_list = list()
    # things_list 填充, 万一给的 things_list 长度不够就自动补充
    if len(things_list) < len(time_list):
        things_list.extend(["尚未安排" for i in range(len(time_list) - len(things_list))])

    for time, things in zip(time_list, things_list):
        time_format = "{}:   {}".format(time, things)
        hour_plan_list.append(time_format)

    return hour_plan_list


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
    :return: ['2016.07.21 周四:', '2016.07.22 周五:', ... ]
    """
    week_days = ["一", "二", "三", "四", "五", "六", "日"]
    date_list = list()
    date = start_date

    for i in range(number):
        year, month, day, week_day = date.year, date.month, date.day, date.weekday()
        format_day = "{}.{}.{} 周{}:".format(year, str(month).zfill(2), str(day).zfill(2), week_days[week_day % 7])
        date_list.append(format_day)

        # 更新下一天
        date += datetime.timedelta(days=1)

    return date_list


if __name__ == "__main__":
    # Java 视频
    # 计算机网络
    # 操作系统
    # 数据库原理
    # Learning how to learn
    # PHP
    # C++
    # 刷题
    # 网络对抗原理
    # 形式逻辑
    # 软件逆向工程
    # 科技信息检索
    # 现代密码学
    # 操作系统原理
    # 计算机网络
    # 软件安全与漏洞分析
    # 网络对抗原理
    # 相关参数设定
    morning_tasks = ["小甲鱼数据结构视频", "数学视频 + 锻炼身体(程序员健康指南)", "日语口语练习"]
    after_noon_tasks = ["大话数据结构", "锻炼身体(运动) + 博客", "百家讲坛/看知乎", "大话数据结构"]
    night_tasks = ["程序员健康指南", "锻炼身体(运动) + 博客"]

    date_plan = create_date(number=200)
    morning_hour_plan = create_format_hour_plan("08:35", "11:30", morning_tasks)
    afternoon_hour_plan = create_format_hour_plan("13:40", "17:30", after_noon_tasks)
    night_hour_plan = create_format_hour_plan("18:40", "21:30", night_tasks)

    # 开始生成
    hour_plan = [morning_hour_plan, afternoon_hour_plan, night_hour_plan]

    with open("result.txt", "w") as f:
        for each_day in date_plan:
            print(each_day, file=f)
            for each_time, each_hour_plan in zip(["早上", "下午", "晚上"], hour_plan):
                print("    {}:".format(each_time), file=f)
                for each_hour in each_hour_plan:
                    print("        {}".format(each_hour), file=f)
            print("", file=f)
