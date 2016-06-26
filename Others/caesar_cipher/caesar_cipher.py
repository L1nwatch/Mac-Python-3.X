#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 再次手搓凯撒密码
"""

__author__ = '__L1n__w@tch'


def caesar_cipher_encrypt(plain_text, shift):
    """
    默认字典为: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
    :param plain_text: 待加密的明文
    :param shift: 偏移
    :return: str()
    """
    dictionary = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    shift %= len(dictionary)
    map_dictionary = dictionary[shift:] + dictionary[:shift]

    cipher_text = str()
    for each_char in plain_text:
        cipher_text += map_dictionary[dictionary.index(each_char)]
    return cipher_text


def caesar_cipher_decrypt(cipher_text, shift):
    """
    默认字典为: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
    :param cipher_text: 待解密的密文
    :param shift: 偏移
    :return: str()
    """
    dictionary = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    shift %= len(dictionary)
    map_dictionary = dictionary[shift:] + dictionary[:shift]

    plain_text = str()
    for each_char in cipher_text:
        plain_text += dictionary[map_dictionary.index(each_char)]
    return plain_text


if __name__ == "__main__":
    pass
