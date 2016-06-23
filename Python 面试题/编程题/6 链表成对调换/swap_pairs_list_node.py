#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 链表成对调换

1->2->3->4 转换成 2->1->4->3

参考 GitHub 给的思路, 其实挺好理解的
"""

__author__ = '__L1n__w@tch'


def swap_pairs(head_node):
    """
    链表成对调换
    :param head_node:
    :return:
    """
    if head_node is not None and head_node.next is not None:
        next_node = head_node.next
        head_node.next = swap_pairs(next_node.next)
        next_node.next = head_node
        return next_node
    return head_node


def print_list_node(head_node):
    """
    顺序打印链表
    :param head_node: 头结点
    :return: None
    """
    for node in list_node:
        print("No.{} List Node, Next: {}".format(node.value, node.next.value if node.next is not None else None))
    print()


class ListNode:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


if __name__ == "__main__":
    list_node = list()
    for i in range(4, 0, -1):
        list_node.append(ListNode(i, list_node[-1] if len(list_node) > 0 else None))
    list_node = list(reversed(list_node))

    print_list_node(list_node[0])

    swap_pairs(list_node[0])
    print_list_node(list_node[0])
