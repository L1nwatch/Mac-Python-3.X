#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
20160827, 实现测试, 先写了一个测试, 看是否能够获取到路径下的所有文件名(指定格式), 另外一个是测试能否正确打开那个文件
"""
import unittest
import subprocess
import random
from random_choicer import get_all_files_path_with_fix, open_a_file_with_right_app, random_choice

__author__ = '__L1n__w@tch'


class TestGetRightFileInfo(unittest.TestCase):
    def test_get_all_files_path(self):
        """
        测试是否能获取到指定路径下的所有指定后缀的文件
        :return:
        """
        test_directory = "/Users/L1n/Desktop/Entertainment/进击的巨人第一季全集"
        files_list = get_all_files_path_with_fix(test_directory, ["mp4", "mp3"])

        # 测试是否能够获取到根路径下的一个文件
        test_file1 = "/Users/L1n/Desktop/Entertainment/进击的巨人第一季全集/[Dymy][Shingeki no Kyojin][17][BIG5][1280X720].mp4"
        self.assertIn(test_file1, files_list)

        # 测试是否获取到格式是想要的格式
        test_file2 = "/Users/L1n/Desktop/Entertainment/进击的巨人第一季全集/[Dymy][Shingeki no Kyojin][17][BIG5][1280X720].txt"
        self.assertNotIn(test_file2, files_list)

        # 测试是否能够获取到子路径下的一个文件
        test_file3 = "/Users/L1n/Desktop/Entertainment/进击的巨人第一季全集/第 18 集/【修罗字幕组】[进击的巨人][18][720P][中日双语字幕].mp4"
        self.assertIn(test_file3, files_list)

    def test_open_a_file_with_right_app(self):
        """
        测试是否能够正确打开一个文件
        :return:
        """
        # test_file = "/Users/L1n/Desktop/Entertainment/进击的巨人第一季全集/[Dymy][Shingeki no Kyojin][07][BIG5][1280X720].mp4"
        test_file = "/Users/L1n/Desktop/Entertainment/进击的巨人第一季全集/第 18 集/【修罗字幕组】[进击的巨人][18][720P][中日双语字幕].mp4"
        open_a_file_with_right_app(test_file)
        with subprocess.Popen("ps -u w@tch | grep mpv", stdout=subprocess.PIPE, shell=True) as proc:
            res = proc.stdout.read()
        self.assertIn(b"/Applications/mpv.app/Contents/MacOS/mpv", res)

    def test_random_choice(self):
        """
        测试是否能够实现随机选择功能
        :return:
        """
        test_list = list()
        for i in range(10):
            test_list.append(random.randint(-1000, 1000))

        result_set = set()
        for j in range(1000):
            result_set.add(random_choice(test_list))
        self.failUnless(len(result_set) == 10)


if __name__ == "__main__":
    pass
