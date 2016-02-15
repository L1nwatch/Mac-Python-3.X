#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

import json

source = r"C:\Users\Administrator.hp-PC\Desktop"
destination = r"E:\good_good_study"
retention_files = ["Software", "网安Subjects", "MathType"]


def main():
    file_name = "configure.json"
    with open(file_name, "w+") as f:
        data = {"source": source, "destination": destination, "retention": retention_files}
        json_data = json.dumps(data, sort_keys=True, indent=4)
        f.write(json_data)

    with open(file_name, "r") as f:
        json_data = f.read()
        data = json.loads(json_data)
        print(data)


if __name__ == "__main__":
    main()
