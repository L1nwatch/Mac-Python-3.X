#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://www.shiyanbar.com/ctf/1872
题目描述:
数列A满足An = An-1 + An-2 + An-3, n >= 3
编写程序，输入A0, A1 和 A2的值1 1 1时, 计算A99的高八位。
key格式：CTF{}

之前信息安全数学基础上有个 Fibonacci,这里自己手动扩展一下吧
'''
__author__ = '__L1n__w@tch'


class Fibonacci:
    def __init__(self, f0, f1, f2):
        self.f0 = f0
        self.f1 = f1
        self.f2 = f2

    def _fib(self, a, b, c):
        a, b, c = a, b, c
        yield a
        yield b
        yield c
        while True:
            a, b, c = b, c, a + b + c
            yield c

    def fib_generator(self):
        return self._fib(self.f0, self.f1, self.f2)

    def get_num(self,n):
        counts = 0
        for num in self.fib_generator():
            counts += 1
            if counts >= n + 1:
                return num


def main():
    f = Fibonacci(1, 1, 1)
    answer = f.get_num(99)
    print(answer)



if __name__ == "__main__":
    main()
