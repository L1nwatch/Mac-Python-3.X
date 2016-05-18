#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 在写的过程中遇到需要 jmp short .... 的汇编指令编写, 目前知道:
    jmp 06 即为 EB 06(从 0x0012FDAA -> 0x0012FDB2),
    EB A6 为 0x0012FDA8 -> 0x0012FD50

听闻 EB 后面的那个字节是补码形式表示的, 所以需要进行补码换算:
已知:
    正数的原码=补码=反码: 1 = 0000 0001

    负数
        -2 原码 = 1000 0010
        -2 补码 = 1111 1110
        -2 反码 = 1111 1101
'''
__author__ = '__L1n__w@tch'


def compute_one_complement(num):
    """
    给一个数字(10 进制表示, 认为是有符号数), 得到其原码
    :param num: 1
    :return: "00000001"
    """
    if num > 127 or num < -127:
        raise RuntimeError("参数有误啊你!")

    # 正数
    if num > 0:
        return bin(num)[2:].zfill(8)
    elif num == 0:
        # +0 -> 0000 0000
        # -0 -> 1000 0000
        return (bin(0)[2:].zfill(8), "1" + bin(0)[2:].zfill(7))
    # 负数
    else:
        # return listbits(num)
        return "1" + bin(num)[3:].zfill(7)


def compute_two_complement(num):
    """
    给一个数字(10 进制表示, 认为是有符号数), 得到其补码
    :param num: 1
    :return: "00000001"
    """
    if num > 127 or num < -128:
        raise RuntimeError("参数有误啊你!")

    # 正数
    if num > 0:
        return bin(num)[2:].zfill(8)
    elif num == 0:
        return bin(0)[2:].zfill(8)
    # 负数
    elif num == -128:
        return "10000000"
    else:
        raw = compute_one_complement(num)
        index = raw.rfind("1")
        res = "1"
        for i in range(1, index):
            if raw[i] == "1":
                res += "0"
            else:
                res += "1"
        return res + raw[index:]


def bit(val, idx):
    """
    测试某个位的值是否是1
    :param val: 0b0101
    :param idx: True
    :return:
    """
    mask = 1 << idx  # all 0 except idx
    return bool(val & mask)  # 注意这里书里面写错写成val & 1了


def listbits(val):
    """
    列出每一位
    :param val:
    :return:
    """
    num = len(bin(val)) - 2
    result = []
    for n in range(num):
        result.append(1 if bit(val, n) else 0)
    return "".join(str(i) for i in list(reversed(result)))


def compute_fan(val):
    pass


if __name__ == "__main__":
    num = -2
    yuan = compute_one_complement(num)
    bu = compute_two_complement(num)
    fan = compute_fan(num)
    print(yuan, bu, fan)
