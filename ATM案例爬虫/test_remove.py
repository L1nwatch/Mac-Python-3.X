#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
import os
import distutils.dir_util

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    path = os.path.join(os.path.abspath(os.curdir), "test_for_crawl")
    distutils.dir_util.remove_tree(path)
