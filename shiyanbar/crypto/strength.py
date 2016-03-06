#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' URL: http://ctf4.shiyanbar.com/crypto/problem.txt
参考WriteUp:  http://grocid.net/

攻击参考 http://diamond.boisestate.edu/~liljanab/ISAS/course_materials/AttacksRSA.pdf
第 2 部分 Common modulus attack
简单来说,同一条消息,经由相同的 N,不同的 e加密(RSA)后得到不同的c;
攻击者只要能够获取 gcd(e1,e2)==1 的两对 n e c 值,就能够还原出 M
还原的方法是利用扩展欧几里德算法,计算出 a*e1 + b*e2 = 1 中的 a 和 b
然后计算 c^a * c^b mod N,就可以还原出 M 来
'''
__author__ = '__L1n__w@tch'

import gmpy2
import binascii


def get_groups_nec(file_name):
    """

    :param file_name: "problem.txt"
    :return: [(n1,e1,c1),(n2,e2,c2),...]
    """
    groups = list()
    with open(file_name, "r") as f:
        f.readline()  # 去掉第一行 {N:E:C}
        for each in f:
            n, e, c = (int(string.strip("{}\r\n\t L")[2:], 16) for string in each.split(":"))
            groups.append((n, e, c))

    return groups


def main():
    groups = get_groups_nec("problem.txt")

    for x in groups:
        for y in groups:
            if x == y:
                continue

            n1, e1, c1 = x
            n2, e2, c2 = y

            # 涉及扩展欧几里德算法
            # 这里的算法得好好学习下, 怎么求出 a 和 b 的
            # a * e1 + b * e2 = 1
            if gmpy2.gcd(e1, e2) == 1:
                a = gmpy2.invert(e1, e2)
                b = int((gmpy2.gcd(e1, e2) - a * e1) / e2)

                assert (a * e1 + b * e2) == 1
                assert b < 0

                c2i = gmpy2.invert(c2, n1)
                c1a = gmpy2.powmod(c1, a, n1)
                c2b = gmpy2.powmod(c2i, -b, n1)
                m = c1a * c2b % n1
                print(binascii.unhexlify(hex(m)[2:]))


if __name__ == "__main__":
    main()
