#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
'''
question1:
    url: http://www.shiyanbar.com/ctf/1862,下下来是个音频文件(解压密码用盲文解得)
question2:
    url: http://www.shiyanbar.com/ctf/1858
一眼看上去就是 16 进制的 ASCII 字符, 解码后得到 EFEF2E2FFEF2FE2
觉得有点像是培根密码, 后来看了 WriteUp 之后才知道了是摩斯码
'''
__author__ = '__L1n__w@tch'

from collections import ChainMap
import binascii


class Morse:
    upper_letters_map = {
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..",
        "E": ".", "F": "..-.", "G": "--.", "H": "....",
        "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
        "M": "--", "N": "-.", "O": "---", "P": ".--.",
        "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
        "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
        "Y": "-.--", "Z": "--.."}

    digits_map = {
        "0": "-----", "1": ".----", "2": "..---", "3": "...--",
        "4": "....-", "5": ".....", "6": "-....", "7": "--...",
        "8": "---..", "9": "----."
    }

    symbols_map = {
        ".": ".-.-.-", ":": "---...", ",": "--..--", ";": "-.-.-.",
        "?": "..--..", "=": "-...-", "'": ".----.", "/": "-..-.",
        "!": "-.-.--", "-": "-....-", "_": "..--.-", "\"": ".-..-.",
        "(": "-.--.", ")": "-.--.-", "$": "...-..-", "&": "....",
        "@": ".--.-."
    }

    # 合并多个字典, 这样不会产生新的字典, 而且这样的字典会随原字典的改变而改变
    all_map = ChainMap(upper_letters_map, digits_map, symbols_map)

    @staticmethod
    def reverse_map(map):
        return dict(zip(map.values(), map.keys()))

    @staticmethod
    def decode_morse(cipher_text):
        """
        :param cipher_text: "-- --- .-. ... ."
        :return: "MORSE"
        """
        groups = cipher_text.split(" ")
        map = Morse.reverse_map(Morse.all_map)
        morse_decoded = str()
        for each in groups:
            try:
                morse_decoded += map[each]
            except:
                morse_decoded += each

        print("Morse decoded: {}".format(morse_decoded))

        return morse_decoded


def question1():
    morse_encoded = "-.-. - ..-. .-- .--. . .. ----- ---.. --... ...-- ..--- ..--.. ..--- ...-- -.. --.."
    Morse.decode_morse(morse_encoded)


def question2():
    cipher_text = "45 46 45 46 32 45 32 46 46 45 46 32 46 45 32"
    cipher_text = cipher_text.replace(" ", "")
    unhex_text = binascii.unhexlify(cipher_text).decode("utf8")
    encoded = unhex_text.replace("E", "-").replace("F", ".").replace("2", " ")
    decoded = Morse.decode_morse(encoded)


def main():
    question1()
    question2()


if __name__ == "__main__":
    main()
