#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
__author__ = '__L1n__w@tch'
''' Class that represents a bit mask.
It has methods representing all the bitwise operations plus some additional features.
The methods return a new BitMask object or a boolean result.
See the bits module for more on the operations provided.
'''


class BitMask(int):
    # 仅仅为类提供新方法而不存储任何额外的数据特性,因此不需要提供一个__new__()构造函数或__init__()初始化函数
    def AND(self, bm):
        return BitMask(self & bm)

    def OR(self, bm):
        return BitMask(self | bm)

    def XOR(self, bm):
        return BitMask(self ^ bm)

    def NOT(self):
        return BitMask(~self)

    def shiftleft(self, num):
        return BitMask(self << num)

    def shiftright(self, num):
        return BitMask(self >> num)

    def bit(self, num):
        mask = 1 << num
        return bool(self & mask)

    def setbit(self, num):
        mask = 1 << num
        return BitMask(self | mask)

    def zerobit(self, num):
        mask = ~(1 << num)
        return BitMask(self & mask)

    def listbits(self, start=0, end=-1):
        end = end if end < 0 else end + 2
        return [int(c) for c in bin(self)[start + 2:end]]


def test():
    bm1 = BitMask()
    print(bm1)
    print(bin(bm1.NOT() & 0xF))
    bm2 = BitMask(0b10101100)
    print(bin(bm2 & 0xFF))
    print(bin(bm2 & 0xF))
    print(bm1.AND(bm2))
    print(bin(bm1.OR(bm2)))
    bm1 = bm1.OR(0b110)
    print(bin(bm1))
    print(bin(bm2))
    print(bin(bm1.XOR(bm2)))
    bm3 = bm1.shiftleft(3)
    print(bin(bm3))
    print(bm1 == bm3.shiftright(3))
    bm4 = BitMask(0b11110000)
    print(bm4.listbits())
    print(bm4.listbits(2, 5))
    print(bm4.listbits(2, -2))


if __name__ == "__main__":
    test()
