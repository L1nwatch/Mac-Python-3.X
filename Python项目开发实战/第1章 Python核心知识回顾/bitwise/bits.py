#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
__author__ = '__L1n__w@tch'
''' 基于整数输入, 位数是从右边开始查的, 起始于0.
Functional wrapper around the bitwise operators.
Designed to make their use more intuitive to users not familiar with the underlying C operators.
Extends the functionality with bitmask read/set operations.

The inputs are integer values and return types are 16 bit integers or boolean.
bit indexes are zero based

Functions implemented are:
    NOT(int)                ->  int
    AND(int, int)           ->  int
    OR(int, int)            ->  int
    XOR(int, int)           ->  int
    shiftleft(int, num)     ->  int
    shiftright(int, num)    ->  int
    bit(int, index)         ->  bool
    setbit(int, index)      ->  int
    zerobit(int, index)     ->  int
    listbits(int, num)      ->  [int, int, ..., int]
'''


def NOT(value):
    return ~value


def AND(val1, val2):
    return val1 & val2


def OR(val1, val2):
    return val1 | val2


def XOR(val1, val2):
    return val1 ^ val2


def shiftleft(val, num):
    return val << num


def shiftright(val, num):
    # Python使用0去填充移位操作留下的空隙
    return val >> num


def bit(val, idx):
    """
    测试某个位的值是否是1
    :param val: 0b0101
    :param idx: True
    :return:
    """
    mask = 1 << idx  # all 0 except idx
    return bool(val & mask)  # 注意这里书里面写错写成val & 1了


def setbit(val, idx):
    """
    设置一位的值为1
    :param val: 0b1000
    :param idx: 1
    :return: 0b1010
    """
    mask = 1 << idx  # all 0 except idx
    return val | mask


def zerobit(val, idx):
    """
    对普通的掩码进行按位补码,从而设置一位的值为0(或者称重置位值)
    :param val: 0b1000
    :param idx: 1
    :return: 0b1000
    """
    mask = ~(1 << idx)  # all 1 except idx
    return val & mask


def listbits(val):
    num = len(bin(val)) - 2
    result = []
    for n in range(num):
        result.append(1 if bit(val, n) else 0)
    return list(reversed(result))


def test():
    print(NOT(0b0101))
    print(bin(NOT(0b0101)))
    # 因为数字是负的,Python在内部会使用最左边的位来表示符号.通过反转所有位,我们可以反转它的符号
    # 0xF只帮助恢复最右的四位, 如果反转的值大于16,则每个十六进制数都需要再多加一个F到掩码后面
    print(bin(NOT(0b0101) & 0xF))
    print(bin(AND(0b0101, 0b0011) & 0xF))
    print(bin(AND(0b0101, 0b0100) & 0xF))
    print(bin(OR(0b0101, 0b0100) & 0xF))
    print(bin(OR(0b0101, 0b0011) & 0xF))
    print(bin(XOR(0b0101, 0b11) & 0xF))
    print(bin(XOR(0b0101, 0b0101) & 0xF))
    print(bin(shiftleft(0b10, 1)))
    print(bin(shiftleft(0b10, 4)))
    print(bin(shiftright(0b1000, 2)))
    print(bin(shiftright(0b1000, 6)))
    print(bit(0b0101, 0))
    print(bit(0b0101, 1))
    print(bin(setbit(0b1000, 1)))
    print(bin(zerobit(0b1000, 1)))
    print(listbits(0b10111))


if __name__ == "__main__":
    test()
