#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 计算上架时间
"""
import datetime

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    start_time = datetime.datetime.strptime("2018-12-04 14:14:00", "%Y-%m-%d %H:%M:%S")
    step = 1659
    nums = 20

    time = start_time
    for i in range(20):
        time += datetime.timedelta(seconds=step)
        print(time)
