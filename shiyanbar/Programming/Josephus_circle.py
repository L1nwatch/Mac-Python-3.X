#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://www.shiyanbar.com/ctf/1866
题目描述: 总共有2 * k个人报数，前面k个是好人，后面k个是坏人，从第一个好人开始报数，报道m的人要死去。
然后从死人的下一个活人继续从头开始报数，报道m的人死去，以此类推。当k = 12时，问m为何值时，坏人全部死去之前不会有好人死去。
'''
__author__ = '__L1n__w@tch'

k = 12


def is_good_all_survice(people):
    global k
    for i in range(1, k + 1):
        try:
            people.index(i)
        except ValueError:
            return False
    return True


def main():
    global k
    init = list()
    for i in range(1, k * 2 + 1):
        init.append(i)

    for m in range(1, 10 ** 10):
        people = list.copy(init)
        pos = 0
        flag = False
        while len(people) > 12:
            pos = (pos + m - 1) % len(people)
            people.pop(pos)
            flag = is_good_all_survice(people)
            if not flag:
                break
        if flag and len(people) == 12:
            print(m, people)
            break


if __name__ == "__main__":
    main()
