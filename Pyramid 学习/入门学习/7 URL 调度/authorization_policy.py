#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 权限认证策略
"""

__author__ = '__L1n__w@tch'


class Article:
    """
    当 xxx/{article} 路径被匹配并且 article 等于 1 时, Pyramid 才会赋予 editor 用户 view 权限
    """

    def __init__(self, request):
        matchdict = request.matchdict
        article = matchdict.get("article", None)
        # if article == "1":
        #     self.__acl__ = [(Allow, "editor", "view")]


if __name__ == "__main__":
    pass
