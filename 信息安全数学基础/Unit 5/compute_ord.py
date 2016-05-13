#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import gmpy2


def compute_order():
    """
    m=2^7*3^4*7^2, a=13, 求 ord_m(a)
    :return:
    """
    m = gmpy2.mpz(2 ** 7 * 3 ** 4 * 7 ** 2)
    a = 13
    phi_m = (2 ** 7 - 2 ** 6) * (3 ** 4 - 3 ** 3) * (7 ** 2 - 7)

    a_list = list()

    for i in range(1, phi_m):
        if m % i == 0:
            a_list.append(i)

    # for i in range(1, m):
    #     if 13 ** i % m == 1:
    #         print(i)
    #         break

    print("m={}".format(m))
    for each in a_list:
        print("13^{}={}".format(int(each), 13 ** int(each) % m))


def compute_order3():
    """
    m=2^7*3^4*7^2, a=13, 求 ord_m(a)
    :return:
    """
    m = gmpy2.mpz(2 ** 5 * 7 ** 4)
    a = 13
    phi_m = (2 ** 5 - 2 ** 4) * (7 ** 4 - 7 ** 3)

    a_list = list()

    for i in range(1, phi_m):
        if m % i == 0:
            a_list.append(i)

    # for i in range(1, m):
    #     if 13 ** i % m == 1:
    #         print(i)
    #         break

    print("m={}\nphi_m={}".format(m, phi_m))
    print("List={}".format(a_list))
    for each in a_list:
        print("13^{}={}".format(int(each), a ** int(each) % m))
        if a ** int(each) % m == 1:
            break


if __name__ == "__main__":
    # compute_order()
    compute_order3()
