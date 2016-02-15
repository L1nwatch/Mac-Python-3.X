#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import json

test_src = r"C:\Users\L1n\Desktop"
test_des = r"D:\goodgoodstudy"
retention = ['desktop.ini', 'Software', 'Study.lnk', '小Q屏幕截图.lnk']


def main():
    file_name = "test_configure.json"
    with open(file_name, "w+") as f:
        data = {"source": test_src, "destination": test_des, "retention": retention}
        json_data = json.dumps(data, sort_keys=True, indent=4)
        f.write(json_data)

    with open(file_name, "r") as f:
        json_data = f.read()
        data = json.loads(json_data)
        print(data)


if __name__ == "__main__":
    main()
