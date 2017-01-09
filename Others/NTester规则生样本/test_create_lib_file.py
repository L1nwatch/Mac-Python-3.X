#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.09 作为测试第三个模块的单元测试文件
"""
import unittest

from pyDes import *
import base64

from create_lib_file import LibCreator

__author__ = '__L1n__w@tch'


class TestCreateLib(unittest.TestCase):
    def setUp(self):
        self.key = b"sangfor!"
        self.iv = b"sangfor*"
        self.lc = LibCreator(self.key, self.iv, "aaa")

    def encrypt(self, data, password):
        if len(password) > 8:
            password = password[0:8]
        aes_obj = des(password, CBC, self.iv, pad=None, padmode=PAD_PKCS5)
        end_data = aes_obj.encrypt(data)
        return base64.b64encode(end_data)

    def decrypt(self, data, password):
        d_data = base64.b64decode(data)
        if len(password) > 8:
            password = password[0:8]
        des_obj = des(password, CBC, self.iv, pad=None, padmode=PAD_PKCS5)
        res_data = des_obj.decrypt(d_data)
        return res_data

    def test_encrypt(self):
        """
        测试加密是否写对了
        """
        plain_text = b'47'
        right_answer = b"hLiRoF26yOA="
        my_answer = self.lc.des_encrypt(plain_text)
        self.assertEqual(right_answer, my_answer)

        plain_text = b"a" * 16
        right_cipher_text = self.encrypt(plain_text, self.key)
        my_answer = self.lc.des_encrypt(plain_text)
        self.assertEqual(right_cipher_text, my_answer)

        plain_text = b"ab" * 16
        right_cipher_text = self.encrypt(plain_text, self.key)
        my_answer = self.lc.des_encrypt(plain_text)
        self.assertEqual(right_cipher_text, my_answer)

        plain_text = b"a" * 7
        right_cipher_text = self.encrypt(plain_text, self.key)
        my_answer = self.lc.des_encrypt(plain_text)
        self.assertEqual(right_cipher_text, my_answer)

        plain_text = b"a" * 8
        right_cipher_text = self.encrypt(plain_text, self.key)
        my_answer = self.lc.des_encrypt(plain_text)
        self.assertEqual(right_cipher_text, my_answer)

        plain_text = b"a" * 9
        right_cipher_text = self.encrypt(plain_text, self.key)
        my_answer = self.lc.des_encrypt(plain_text)
        self.assertEqual(right_cipher_text, my_answer)

    def test_decrypt(self):
        """
        测试解密是否正确
        """
        right_plain_text = b"a" * 16
        cipher_text = self.encrypt(right_plain_text, self.key)
        my_answer = self.lc.des_decrypt(cipher_text)
        wb_answer = self.decrypt(cipher_text, self.key)
        self.assertEqual(right_plain_text, my_answer)
        self.assertEqual(my_answer, wb_answer)


if __name__ == "__main__":
    pass
