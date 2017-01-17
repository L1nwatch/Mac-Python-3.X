#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.17 作为读取配置文件的测试文件
"""
import unittest
from common_basic import ConfigReader

__author__ = '__L1n__w@tch'


class TestConfigReader(unittest.TestCase):
    def setUp(self):
        self.test_file_path = "config_file_for_test.conf"
        self.test_cr = ConfigReader(self.test_file_path)

    def test_read_mysql_info(self):
        """
        测试读取 mysql 信息
        """
        db_host, db_user, db_password, db_name = self.test_cr.read_mysql_info()
        self.assertEqual(db_host, "192.192.90.134")
        self.assertEqual(db_user, "root")
        self.assertEqual(db_password, "root")
        self.assertEqual(db_name, "FW_LOG_fwlog")

    def test_read_af_info(self):
        """
        测试读取 af 信息
        """
        af_ip, af_port, af_back_user, af_back_password = self.test_cr.read_af_back_info()
        self.assertEqual(af_ip, "192.192.90.134")
        self.assertEqual(af_port, 22345)
        self.assertEqual(af_back_user, "admin")
        self.assertEqual(af_back_password, "1")

    def test_read_ip_info(self):
        """
        测试读取 ip 信息
        """
        local_ip, target_ip = self.test_cr.read_ip_info()
        self.assertEqual(local_ip, "192.192.88.135")
        self.assertEqual(target_ip, "192.168.116.2")

    def test_read_des_info(self):
        """
        测试读取 des 相关信息
        """
        des_key, des_iv = self.test_cr.read_des_info()
        self.assertEqual(des_key, "sangfor!")
        self.assertEqual(des_iv, "sangfor*")

    def test_read_lib_info(self):
        """
        测试读取 lib 相关信息
        """
        lib, waf_ips, utm = self.test_cr.read_lib_info()
        self.assertEqual(lib, "test.lib")
        self.assertEqual(waf_ips, "sample_waf_ips")
        self.assertEqual(utm, "sample_utm")


if __name__ == "__main__":
    pass
