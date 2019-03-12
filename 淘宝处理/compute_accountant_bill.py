#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 自动化计算账单
"""

__author__ = '__L1n__w@tch'


def check_cost_money(product_title, product_sku):
    """
    检查商品成本
    :param product_title: 商品标题
    :param product_sku: 商品分类
    :return:
    """
    if product_sku == "-" or product_title == "":
        return "0"

    cost_money = "??"
    money_map = {
        '美逸/MEIYI充电宝20000M毫安大容量快充便携移动电源Type-C手机PD': {
            "-": "0",
            '"颜色分类：GT20白骑士[QC3.0快充]"': "98",
            '"颜色分类：黑色[GT20黑金刚]"': "108",
            '"颜色分类：白色[GT20白骑士]"': "98",
            '"颜色分类：乳白色[GT20原色]"': "89",
        },
        '美逸大容量手机充电宝30000毫安聚合物电芯数显移动电源多USB口通': {
            "-": "0",
            '"颜色分类：乳白色"': "109",
            '"颜色分类：白色"': "109",
        },
        '美逸/MEIYI苹果数据线iPhoneXPlus充电器ios手机平板ipad2M快充短': {
            "-": "0",
            '"长度：2m;颜色分类：苹果ios樱花粉[【1m】提速70%]"': "!!",
            '"长度：2m;颜色分类：安卓micro樱花粉[【2m】提速70%]"': "!!",
            '"长度：1m;颜色分类：苹果ios樱花粉[【1m】提速70%]"': "!!",
            '"长度：2m;颜色分类：安卓micro玫瑰金[【1m】提速50%]"': "!!",
            '"长度：2m;颜色分类：苹果ios岩石灰[【1m】提速70%]"': "!!",
            '"长度：2m;颜色分类：安卓micro天空蓝[【2m】提速70%]"': "!!",
            '"长度：1m;颜色分类：安卓micro樱花粉[【2m】提速70%]"': "!!",
            '"长度：0.5m;颜色分类：苹果ios湖水绿[【1m】提速70%]"': "!!",
            '"长度：1.5m;颜色分类：安卓micro樱花粉[【2m】提速70%]"': "!!",
            '"长度：1.5m;颜色分类：苹果ios樱花粉[【1m】提速70%]"': "!!",
            '"长度：1.5m;颜色分类：安卓type-c钛空灰[【1m】提速50%]"': "!!",
            '"长度：0.5m;颜色分类：苹果ios樱花粉[【1m】提速70%]"': "!!",
            '"长度：2m;颜色分类：苹果ios金橙黄[【1m】提速70%]"': "!!",
            '"长度：1m;颜色分类：安卓micro钛空灰[【1m】提速50%]"': "!!",
            '"长度：2m;颜色分类：苹果ios玫瑰金[【0.5m】提速50%]"': "!!",
            '"长度：0.5m;颜色分类：安卓micro玫瑰金[【1m】提速50%]"': "!!",
        },
    }
    # 改了标题了,但是是同样的产品
    money_map['美逸苹果6s六数据线iPhone7px8Plus安卓手机平板ipad2快充线2米短'] = money_map['美逸/MEIYI苹果数据线iPhoneXPlus充电器ios手机平板ipad2M快充短']
    money_map['美逸/MEIYI苹果数据线iPhoneXPlus充电器ios手机平板ipad2M快充短，美逸/MEIYI苹果数据线iPhoneXPlus充电器ios手机平板ipad2M快充短'] = money_map[
        '美逸/MEIYI苹果数据线iPhoneXPlus充电器ios手机平板ipad2M快充短']
    money_map['美逸苹果6s六数据线iPhone7px8Plus安卓手机平板ipad2快充线2米短，美逸苹果6s六数据线iPhone7px8Plus安卓手机平板ipad2快充线2米短'] = money_map[
        '美逸/MEIYI苹果数据线iPhoneXPlus充电器ios手机平板ipad2M快充短']
    money_map['美逸20000毫安充电宝双向快充移动电源LED数显屏高通认证QC3.0/PD'] = money_map['美逸/MEIYI充电宝20000M毫安大容量快充便携移动电源Type-C手机PD']
    cost_money = money_map[product_title][product_sku]

    return cost_money


def get_order_detail_list_info(info_path):
    """
    获取订单详情
    :param info_path:
    :return:
    """
    all_order_details = dict()
    with open(info_path, encoding="utf8") as f:
        for i, each_detail in enumerate(f):
            if i == 0:
                continue
            all_data = each_detail.split(",")
            order_number = str(all_data[0].strip('="'))
            product_sku = all_data[5]
            all_order_details[order_number] = {"product_sku": product_sku}
    return all_order_details


def get_order_list_info(info_path):
    all_orders = list()
    with open(info_path)  as f:
        for i, each_line in enumerate(f):
            if i == 0:
                continue
            all_data = each_line.split(",")
            order_number = all_data[0].strip('="')
            list_date = all_data[19]

            # 未成功销售订单初始化
            event = all_data[29]
            earn_money = "0"

            # 成功销售的订单
            if all_data[29] != "买家未付款" and all_data[29] != "退款":
                event = "销售"
                earn_money = all_data[8]

            product = all_data[21].strip('="')
            sell_number = all_data[26]

            pay_people = "黄家进"
            clear_state = "未结算"
            comment = all_data[1]
            all_orders.append(
                {
                    "list_date": list_date, "order_number": order_number, "product": product,
                    "event": event, "sell_number": sell_number, "earn_money": earn_money, "pay_people": pay_people,
                    "clear_state": clear_state, "comment": comment,
                }
            )
    return all_orders


if __name__ == "__main__":
    info_path = "./input/ExportOrderList201903121048.csv"
    detail_path = "./input/ExportOrderDetailList201903121048.csv"

    # 获取订单信息
    all_orders = get_order_list_info(info_path)
    all_order_details = get_order_detail_list_info(detail_path)

    # 输出统计结果
    with open("./output/accountant_bill.csv", "w", encoding="utf8") as f:
        titles = ["日期", "订单号", "事项", "商品", "型号", "数量", "支出金额", "收入金额", "付款人", "结算情况", "备注"]
        f.write("{}\n".format(",".join(titles)))
        for each_order in all_orders:
            product = each_order["product"]
            product_sku = all_order_details.get(each_order["order_number"], {"product_sku": "-"})["product_sku"]

            write_info = [
                each_order["list_date"],
                "{}_".format(each_order["order_number"]),
                each_order["event"],
                product,
                product_sku,
                each_order["sell_number"],
                check_cost_money(product, product_sku),
                each_order["earn_money"],
                each_order["pay_people"],
                each_order["clear_state"],
                each_order["comment"],
                # "?",
            ]
            f.write("{}\n".format(",".join(write_info)))
