#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 处理同花顺

http://stockpage.10jqka.com.cn/000629/
http://stockpage.10jqka.com.cn/realHead_v2.html#hs_000629
http://d.10jqka.com.cn/v2/realhead/hs_000629/last.js

市盈率:http://www.iwencai.com/stockpick/search?preParams=&ts=1&qs=zgxgrh_syl&tid=stockpick&w=++%E5%B8%82%E7%9B%88%E7%8E%87%28pe%29

"""
import datetime
import os
import re
import time

from selenium import webdriver

__author__ = '__L1n__w@tch'

browser = None
this_month = datetime.datetime.today().strftime("%Y-%m")
this_month_log_path = "./stock_log/{}".format(this_month)
today = datetime.datetime.today().strftime("%Y-%m-%d")
this_day_log_path_day = "./stock_log/{}/{}_result_day.txt".format(this_month, today)
this_day_log_path_week = "./stock_log/{}/{}_result_week.txt".format(this_month, today)


def get_prices_using_number(number, day_step=True):
    """
    根据股票代码,打印出日 K 线里面最低、最高、当前价格
    :param number:
    :param day_step:
    :return:
    """
    global browser
    browser.get("http://stockpage.10jqka.com.cn/realHead_v2.html#{}".format(number))
    cur_result = re.findall(r'<span class="price" id="hexm_curPrice">(.*)</span>', browser.page_source)[0]

    try_times = 0
    while cur_result == "--":
        time.sleep(1)
        cur_result = re.findall(r'<span class="price" id="hexm_curPrice">(.*)</span>', browser.page_source)[0]
        if 'id="quote_header2" style="display:none"' not in browser.page_source or '<strong id="pprice">--</strong>' in browser.page_source:
            print("[-] 股票代码: {}, 已经停牌".format(number))
            browser.refresh()
            try_times += 1
        if try_times > 3:
            return None

    browser.get("http://stockpage.10jqka.com.cn/HQ_v4.html#{}".format(number))
    time.sleep(1)
    for each_element in browser.find_elements_by_class_name("kline-type"):
        if day_step:
            if each_element.text == "日K线":
                each_element.click()
                break
        else:
            if each_element.text == "周K线":
                each_element.click()
                break

    while "hxc3-klineprice-min" not in browser.page_source:
        time.sleep(1)

    max_result = re.findall(r'<div class="hxc3-klineprice-max"[^>]*>([^<]*)</div>', browser.page_source)[0]
    min_result = re.findall(r'<div class="hxc3-klineprice-min"[^>]*>([^<]*)</div>', browser.page_source)[0]

    string = "[*] 股票代码: {},  当前价为: {}, 最高价为: {}, 最低价为: {}".format(number, cur_result, max_result, min_result)
    print(string)

    with open("test.html", "w") as f:
        f.write(browser.page_source)

    return string


def get_all_number():
    """
    访问 数据中心 最近的 业绩预告, 获取所有股票代码
    :return:
    """
    global browser

    # url = "http://data.10jqka.com.cn/financial/yjyg/"
    result = list()
    for i in range(3):
        url = ("http://data.10jqka.com.cn/ajax/yjyg/date/2018-06-30/board/ALL/field/enddate/order/desc/"
               "page/{}/ajax/1/").format(i + 1)
        browser.get(url)
        result.extend(re.findall('<a href="http://stockpage.10jqka.com.cn/\d*/finance/" target="_blank">(\d*)</a>',
                                 browser.page_source))

    return result


def get_prices(day_step=True):
    """
    获取所有业绩预告的股票代码,并获取对应的当前值、最高值、最低值
    :param day_step:
    :return:
    """
    if day_step:
        log_path = this_day_log_path_day
    else:
        log_path = this_day_log_path_week

    global browser
    browser = webdriver.Chrome(
        "/Users/L1n/Desktop/Code/Python/my_blog_source/virtual/selenium/webdriver/chromedriver",
    )

    # finish_list = list()
    # with open(log_path) as f:
    #     for each_line in f:
    #         finish_list.append(each_line[13:19])

    numbers = get_all_number()
    os.makedirs(this_month_log_path, exist_ok=True)
    with open(log_path, "w") as f:
        for each_number in numbers:
            # if each_number in finish_list:
            #     continue
            string = get_prices_using_number("hs_{}".format(each_number), day_step)
            if string:
                print(string, file=f, flush=True)

    browser.quit()


def analysis_prices(day_step=True):
    if day_step:
        log_path = this_day_log_path_day
    else:
        log_path = this_day_log_path_week

    data = list()
    with open(log_path) as f:
        for each_line in f:
            number, cur_price, high_price, low_price = each_line.split(",")
            number = number[13:]
            cur_price = float(cur_price[8:])
            high_price = float(high_price[7:])
            low_price = float(low_price[7:])
            info = {"number": number, "cur_price": cur_price, "high_price": high_price, "low_price": low_price,
                    "sep_low": (cur_price - low_price) * 1.0 / low_price,
                    "sep_high": (high_price - cur_price) * 1.0 / cur_price}
            data.append(info)
    data = sorted(data, key=lambda x: x["sep_low"])

    with open(log_path, "a") as f:
        print("\n[!] {sep} 开始过滤 {sep}\n".format(sep="=" * 30), file=f)

        for each_data in data:
            if str(each_data["number"]).startswith("300"):
                # 跳过创业板
                continue

            print("[*] 股票代码: {}, 离最低点差值: {:.2%}, 离最高点差值: {:.2%}, 当前价格: {}, 最低价格: {}, 最高价格: {}".format(
                each_data["number"], each_data["sep_low"], each_data["sep_high"], each_data["cur_price"],
                each_data["low_price"], each_data["high_price"]), file=f)


if __name__ == "__main__":
    print("[*] {sep} 先获取日 K 线的结果 {sep}".format(sep="=" * 30))
    # get_prices()
    analysis_prices()

    print("[*] {sep} 再获取周 K 线的结果 {sep}".format(sep="=" * 30))

    # get_prices(day_step=False)
    analysis_prices(day_step=False)
