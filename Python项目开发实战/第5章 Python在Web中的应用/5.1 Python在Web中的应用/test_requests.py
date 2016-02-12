#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Mac OS X Python3.4.4下测试requests库
'''
__author__ = '__L1n__w@tch'

import requests


def main():
    # 使用USDA的API搜索了特定ZIP码内的农贸市场
    url = requests.get("http://search.ams.usda.gov/farmersmarkets/v1/data.svc/zipSearch?zip=46201")
    print(url)

    # 在示例中GET到的是json对象
    results = url.json()
    print(results)

    for result in results["results"]:
        print(result)

    # 根据USDA的API文档(http://search.ams.usda.gov/farmersmarkets/v1/svcdesc.html),如果传入一个
    # 之前查询中获得的市场ID,这个搜索会返回一些有关该市场的详情.结果中包含了一个Google地图的链接.
    market = "http://search.ams.usda.gov/farmersmarkets/v1/data.svc/mktDetail?id="
    for result in results["results"]:
        id = result["id"]
        details = requests.get(market + id).json()
        print(details["marketdetails"]["GoogleLink"])


if __name__ == "__main__":
    main()
