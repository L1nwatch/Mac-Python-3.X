#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 网易云课堂上的一道题, 考斐波那契数列, 居然考我 21 之后的数是啥
参考 URL: http://stackoverflow.com/questions/494594/how-to-write-the-fibonacci-sequence-in-python
'''
__author__ = '__L1n__w@tch'


class Fibonacci:
    def __init__(self, f0, f1):
        self.f0 = f0
        self.f1 = f1

    def _fib(self, a, b):
        a = self.f0
        b = self.f1
        yield a
        yield b
        while True:
            a, b = b, a + b
            yield b

    def fib_generator(self):
        return self._fib(self.f0, self.f1)


def main():
    a = Fibonacci(1, 1).fib_generator()
    for each in a:
        print(each, end=" ")
        if each > 100:
            exit()


if __name__ == "__main__":
    main()
