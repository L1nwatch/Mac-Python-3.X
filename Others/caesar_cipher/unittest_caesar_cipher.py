#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 想试着用 unittest 再次试一下自己编写凯撒的能力, 这是测试文件
"""
import unittest
from caesar_cipher import caesar_cipher_encrypt

__author__ = '__L1n__w@tch'


class TestCaesar(unittest.TestCase):
    def setUp(self):
        self.test_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        self.shift = 28
        self.answer_string = "cdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZab"

    def test_caesar(self):
        cipher_text = caesar_cipher_encrypt(self.test_string, self.shift)
        self.failUnless(cipher_text == self.answer_string)


if __name__ == "__main__":
    unittest.main()
