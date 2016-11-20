#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2016.11.20 作为常量文件
"""

__author__ = '__L1n__w@tch'


class _Const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const.{}".format(name))
        if not name.isupper():
            raise self.ConstCaseError("const name {} is not all uppercase".format(name))
        self.__dict__[name] = value


const = _Const()
const.SUCCESS_MESSAGE = "Download success!"
const.CONTINUE_RUN_TIME_LIMIT = "Too Fast!"

if __name__ == "__main__":
    pass
