#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 英文名：The Rail-Fence Cipher
"""
__author__ = '__L1n__w@tch'

from itertools import zip_longest


def main():
    num = 2
    zhalaner = ZhaLan(num)
    ciphertext = zhalaner.encrypt("cATNfs{HtuI}")
    plaintext = zhalaner.decrypt(ciphertext)
    print("plaintext = {0}\n{num}-ciphertext = {1}".format(plaintext, ciphertext, num=num))


class ZhaLan:
    def __init__(self, num):
        self.num = num

    def encrypt(self, plaintext):
        if len(plaintext) % self.num != 0:
            raise RuntimeError
        ciphertext = ""
        for i in range(self.num):
            for each in self._divide_group(plaintext, self.num):
                ciphertext += each[i]

        return ciphertext

    def decrypt(self, ciphertext):
        if len(ciphertext) % self.num != 0:
            raise RuntimeError
        plaintext = ""
        for i in range(len(ciphertext) // self.num):
            for each in self._divide_group(ciphertext, len(ciphertext) // self.num):
                plaintext += each[i]

        return plaintext

    def _divide_group(self, text, size):
        args = [iter(text)] * size
        blocks = list()
        for block in zip_longest(*args):
            blocks.append("".join(block))

        return blocks


if __name__ == "__main__":
    main()

