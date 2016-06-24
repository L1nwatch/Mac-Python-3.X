#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 给定一个数组, 构建二叉树, 并且按层次打印这个二叉树, 以及进行深度遍历
"""
import queue
from functools import wraps

__author__ = '__L1n__w@tch'


def decorator_with_argument(sentence):
    """
    带有一个参数的修饰器
    :param sentence: 要打印的句子
    :return: 修饰器
    """

    def decorator(function):
        @wraps(function)
        def wrap(root):
            print(sentence)
            function(root)
            print("")

        return wrap

    return decorator


class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


@decorator_with_argument("第一种层次遍历")
def layer_search(root):
    """
    层次遍历
    :param root: 根节点
    :return: None
    """
    stack = [root]
    while stack:
        current = stack.pop(0)
        print(current.data, end=" ")
        if current.left:
            stack.append(current.left)
        if current.right:
            stack.append(current.right)


@decorator_with_argument("第二种层次遍历")
def layer_order_traverse(root):
    """
    层次遍历第二种写法, 其实就换了个数据结构
    :param root: 根节点
    :return: None
    """
    a_queue = queue.Queue()
    a_queue.put(root)
    while not a_queue.empty():
        node = a_queue.get()
        print(node.data, end=" ")
        if node.left:
            a_queue.put(node.left)
        if node.right:
            a_queue.put(node.right)


@decorator_with_argument("先序遍历")
def pre_order_traverse(root):
    """
    深度遍历, 先序遍历?
    PS: 之所以把递归封装起来是为了不重复调用装饰器
    :param root: 根节点
    :return: None
    """

    def __recursion(node):
        if not node:
            return None
        print(node.data, end=" ")
        __recursion(node.left)
        __recursion(node.right)

    return __recursion(root)


@decorator_with_argument("中序遍历")
def in_order_traverse(root):
    """
    中序遍历
    :param root: 根节点
    :return: None
    """

    def __recursion(node):
        if not node:
            return None
        if node.left:
            __recursion(node.left)
        print(node.data, end=" ")
        if node.right:
            __recursion(node.right)

    return __recursion(root)


@decorator_with_argument("后序遍历")
def post_order_traverse(root):
    """
    后序遍历
    :param root: 根节点
    :return: None
    """

    def __recursion(node):
        if not node:
            return None
        if node.left:
            __recursion(node.left)
        if node.right:
            __recursion(node.right)
        print(node.data, end=" ")

    return __recursion(root)


if __name__ == "__main__":
    tree = Node(1, Node(3, Node(7, Node(0)), Node(6)), Node(2, Node(5), Node(4)))
    layer_search(tree)
    layer_order_traverse(tree)
    pre_order_traverse(tree)
    in_order_traverse(tree)
    post_order_traverse(tree)
