#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://www.shiyanbar.com/ctf/1867
题目描述: 小白发现了一段很6的字符：NlEyQd{seft}

最后的 Flag 就是 CTF{tianshu} 居然要区分大小写的...
'''
__author__ = '__L1n__w@tch'

import string
from itertools import zip_longest


class Caesar:
    def __init__(self, chars, text):
        self.raw_data = text
        self.chars = chars

    def encrypt(self, shift):
        cipher_text = str()
        for each in self.raw_data:
            if each in self.chars:
                cipher_text += self.chars[(self.chars.index(each) + shift) % len(self.chars)]
            else:
                cipher_text += each

        return cipher_text

    def decrypt(self, shift):
        return self.encrypt(-shift)

    def search(self, string):
        def _check(text):
            text = text.lower()
            for each in string.lower():
                if text.find(each) <= -1:
                    return False
            return True

        texts = list()
        for i in range(len(self.chars)):
            text = self.encrypt(i)
            if _check(text):
                texts.append((i, text))

        return texts


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


def main():
    cipher_text = "NlEyQd{seft}"
    chars = string.ascii_letters
    rail_fence_list = Caesar(chars, cipher_text).search("ctf")
    decrypt_sir = ZhaLan(2)
    for each in rail_fence_list:
        text = decrypt_sir.encrypt(each[1])
        print(text)


if __name__ == "__main__":
    main()
