#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
__author__ = '__L1n__w@tch'
''' Description
'''

import bitwise.bits as bits
from bitwise import bitmask


def main():
    print(bits)
    print(bitmask)
    print(bin(bits.AND(0b1010, 0b1100)))
    print(bin(bits.OR(0b1010, 0b1100)))
    print(bin(bits.NOT(0b1010)))
    print(bin(bits.NOT(0b1010) & 0xFF))
    print(bin(bits.NOT(0b1010) & 0xF))
    bm = bitmask.BitMask(0b1100)
    print(bin(bm))
    print(bin(bm.AND(0b1110)))
    print(bin(bm.OR(0b1110)))
    print(bm.listbits())


if __name__ == "__main__":
    main()
