#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 孙子定理的一道题
'''
__author__ = '__L1n__w@tch'

import gmpy2


def main():
    # 我需要知道求模逆的算法(欧几里德?往下推求得最大公约数,再往回推求得模逆)

    m1, m2 = 11, 23
    a1, a2 = 9, 1
    M1 = m1 * m2 / m1
    M2 = m1 * m2 / m2

    M1_inverse = gmpy2.invert(gmpy2.mpz(M1), m1)
    M2_inverse = gmpy2.invert(gmpy2.mpz(M2), m2)
    print(M1_inverse)
    print(M2_inverse)

    res = (M1 * M1_inverse * a1 + M2 * M2_inverse * a2) % (m1 * m2)
    print(res)


if __name__ == "__main__":
    main()
