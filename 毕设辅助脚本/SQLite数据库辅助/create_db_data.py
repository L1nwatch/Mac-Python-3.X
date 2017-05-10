#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 负责新建 sqlite3 数据库, 以及插入对应的链接关系库, 以便毕设进行查询访问等操作

2017.05.09 统一实际数据库和伪造数据库, 主要是统一表格 DomainID2URLInDoc, 之后 LinkInDoc 采用各自的数据
2017.05.06 新增伪造链接的相关统计代码, 方便伪造控制
2017.05.05 编写代码, 自己伪造关系链接库
2017.03.21 DomainID2URL 依旧存在好多冗余, 过滤一下
2017.03.20 发现数据源里面好多链接冗余, 于是特殊处理一下
2017.03.20 实现新建 sqlite3 数据库以及伪造部分链接关系数据, 另外顺便学习一下 peewee
"""
import sqlite3
import peewee
import os
import re
import random
import bisect
from collections import defaultdict

from xml2json import get_docs_from_file, parse_doc_to_dict, extract_domain_from_url

__author__ = '__L1n__w@tch'

database_name = "/Users/L1n/Desktop/Notes/毕设/毕设实现/工程文件/link_relationship.db"
id2url_file = os.path.join("/Users/L1n/Desktop/Notes/毕设/毕设实现/工程文件/SogouT-Link.v1", "id2url.link")
link_file = os.path.join("/Users/L1n/Desktop/Notes/毕设/毕设实现/工程文件/SogouT-Link.v1", "SogouT-link")
doc_file = os.path.join("/Users/L1n/Desktop/Code/Python/PyCharm/毕设辅助脚本/xml转json", "news_tensite_xml.dat")
evaluate_file = os.path.join("/Users/L1n/Desktop/Notes/毕设/毕设实现/工程文件", "网页搜索结果评价-完整版.txt")


class LinkRelationShip(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase(database_name)

    page_id = peewee.CharField()
    out_id = peewee.CharField()


class PageID2URL(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase(database_name)

    page_id = peewee.CharField(null=False)
    page_url = peewee.TextField(null=False)


class DomainID2URL(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase(database_name)

    page_id = peewee.CharField(null=False)
    page_url = peewee.TextField(null=False)


class LinkInDoc(peewee.Model):
    """
    用于存放与 Doc 中的网页有关联的那些链接关系
    """

    class Meta:
        database = peewee.SqliteDatabase(database_name)

    domain_id = peewee.CharField(null=False)
    out_id = peewee.CharField(null=True)  # 某 domain_id 指向了 xxx


class DomainID2URLInDoc(peewee.Model):
    """
    将域名 id 转换为 url 的表
    """

    class Meta:
        database = peewee.SqliteDatabase(database_name)

    order_id = peewee.IntegerField(null=False, unique=True, primary_key=True)
    page_id = peewee.CharField(null=False)
    page_url = peewee.TextField(null=False)


class WeightRandom:
    def __init__(self, items):
        weights = [w for _, w in items]
        self.goods = [x for x, _ in items]
        self.total = sum(weights)
        self.acc = list(self.accumulate(weights))

    @staticmethod
    def accumulate(weights):  # 累和.如accumulate([10,40,50])->[10,50,100]
        cur = 0
        for w in weights:
            cur = cur + w
            yield cur

    def __call__(self):
        return self.goods[bisect.bisect_right(self.acc, random.uniform(0, self.total))]


class DatabaseBasicDeal:
    def __init__(self):
        # 用来保存存在于 doc 中的 域名 id 映射
        self.doc_domain_id_url_dict = dict()

    @staticmethod
    def create_database():
        """
        负责创建 sqlite3 数据库, 如果已存在则进行连接操作
        :return: sqlite3 的 db 实例
        """
        db = sqlite3.connect(database_name)
        return db

    @staticmethod
    def clear_database(tables):
        """
        清除指定表
        :param tables: list(), 每个是表的类, 比如 []
        :return: None
        """
        print("[*] 执行清除数据库操作")
        # 确保表和库存在, 之后清除数据后重建表
        for each_table in tables:
            if each_table.table_exists():
                # 清除原来的数据
                each_table.drop_table()
                each_table.create_table()
            else:
                each_table.create_table()

    @staticmethod
    def get_all_domain_id_in_doc(file_path):
        """
        从数据源中获取所有文档的域名 id
        :param file_path: str(), 数据源的路径, 比如 "../news_tensite_xml.dat"
        :return: 此函数为生成器, 每次返回一个域名 id
        """
        for each_doc in get_docs_from_file(file_path):
            doc_dict = parse_doc_to_dict(each_doc)
            domain_id = doc_dict["doc_number"].split("-")[1]
            yield domain_id, extract_domain_from_url(doc_dict["url"])

    def get_domain_id_dict_in_doc(self):
        """
        获取所有 doc 中的域名 id
        总共有域名 286 个, 每个域名类似于: "shop.people.com.cn"
        :return: set(), 过滤重复域名 id
        """
        result_dict = dict()
        for i, (each_domain, domain_url) in enumerate(self.get_all_domain_id_in_doc(doc_file)):
            if each_domain not in result_dict:
                progress = ((i + 1) / 1294233) * 100
                print("[*] 进度: {:.2f}%, 找到域名: {}, URL 为: {}".format(progress, each_domain, domain_url))
                result_dict[each_domain] = domain_url

        return result_dict

    def create_domain_id_2_url_in_doc_table_data(self):
        """
        完成清除数据、获取 doc_domain_id_url_dict、写入到数据库
        :return: None, 直接写入到数据库
        """
        self.doc_domain_id_url_dict = self.get_domain_id_dict_in_doc()
        print("[*] 总共有域名: {}".format(len(self.doc_domain_id_url_dict)))

        # 创建 domainid2urlindoc
        print("[*] 开始将数据写入到数据库的 DomainID2URLInDoc 表中")
        self.create_domainid_to_url_in_doc_table(self.doc_domain_id_url_dict)

    @staticmethod
    def create_domainid_to_url_in_doc_table(domain_url_dict):
        """
        创建该表: DomainID2URLInDoc
        其中的数据类似于:
            page_id: "fa7f32f06cef7000"
            page_url: "ah.people.com.cn"
        :param domain_url_dict: dict(), {"domain_id": "url", ...}
        :return: None, 直接写入数据到数据库中
        """
        print("[*] 开始写入数据到表格: DomainID2URLInDoc")
        for i, (each_domain, each_url) in enumerate(domain_url_dict.items()):
            DomainID2URLInDoc.insert({"page_id": each_domain, "page_url": each_url}).execute()

    @staticmethod
    def get_all_domain_id_url_in_doc_from_db():
        """
        之前是从文件里获取所有域名 id, 现在已经把这部分信息写入到数据库了, 所以就从数据库中读取出来即可
        :return: dict(), {domain_id: domain_url, ...}
        """
        domain_info_dict = dict()

        for each_row in DomainID2URLInDoc.select():
            domain_info_dict[each_row.page_id] = each_row.page_url

        return domain_info_dict


class RealDatabase(DatabaseBasicDeal):
    @staticmethod
    def _special_deal(data, choice=1):
        """
        主要针对表 LinkRelationShip, 只保留域名到域名的指向关系
        :param data: str(), 需要处理的数据, 比如 "6a4c0d0f7adf1d20-6ef9b1edc1c18510	6a4c0d0f7adf1d20-6ef9b1edc1c18510"
        :param choice: int(), 表明是什么特殊处理方法
        :return: str(), 处理过后的数据, 比如 "6ef9b1edc1c18510\t6ef9b1edc1c18510"
        """
        if choice == 1:
            # 表明是 LinkRelationShip 的特殊处理
            source, destination = data.split("\t")
            source, destination = source.split("-")[1], destination.split("-")[1]
        else:
            # 表明是 DomainID2URL 的特殊处理
            source, destination = data.split("\t")
            source = source.split("-")[1]
        return "{}\t{}".format(source, destination)

    def read_file_data(self, file_name, field_name, need_special_deal=0):
        """
        读取文件中的每一行, 按空格间隔后返回
        每次读取 1w 行
        :param file_name: str(), 比如 "link_relationship.txt"
        :param field_name: 从文件里读取的每一列的含义
        :param need_special_deal: int(), 区分一下是否需要特殊处理, 0 表示不用特殊处理
        :return: tuple, (str(), str()), 比如 ("1", "https://1.html")
        """
        with open(file_name, "r") as f:
            counts = 0
            temp_list = list()
            for each_line in f:
                counts += 1
                if need_special_deal != 0:
                    each_line = self._special_deal(each_line, need_special_deal)
                temp_list.append({key: value.strip() for key, value in zip(field_name, each_line.split("\t"))})
                if counts == 400:
                    yield temp_list
                    del temp_list[:]
                    counts = 0
                    # temp_list.clear() # python3.2 居然没有这个方法

    def create_link_relationship_db(self):
        """
        负责创建链接数据库相关的表, 插入或更新数据等操作
        :return: None
        """
        # 创建 ID2URL 的数据
        file_path = id2url_file
        print("[*] 读取文件 {} 并插入表 PageID2URL".format(str(file_path).rsplit("/", maxsplit=1)[1]))
        for data_source_list in self.read_file_data(file_path, ["page_id", "page_url"]):
            PageID2URL.insert_many(data_source_list).execute()

        print("[*] 读取文件 {} 并插入表 DomainID2URL".format(str(file_path).rsplit("/", maxsplit=1)[1]))
        for data_source_list in self.read_file_data(file_path, ["page_id", "page_url"], need_special_deal=2):
            DomainID2URL.insert_many(data_source_list).execute()

        # 创建 LinkRelationship 数据
        file_path = link_file
        print("[*] 读取文件 {} 并插入数据库".format(str(file_path).rsplit("/", maxsplit=1)[1]))
        for data_source_list in self.read_file_data(file_path, ["page_id", "out_id"], need_special_deal=1):
            LinkRelationShip.insert_many(data_source_list).execute()

    def run(self):
        # 创建数据库
        self.create_database()

        # 创建链接数据
        confirm = input("[+] 即将修改数据库中的数据, 确认?[y/n]")
        if confirm.lower() == "y":
            # 确保表和库存在, 且为初始状态
            self.clear_database([LinkRelationShip, PageID2URL, DomainID2URL, LinkInDoc, DomainID2URLInDoc])

            # 从文件中读取相应数据后存放到数据库中
            self.create_link_relationship_db()

            # 将数据库中的数据与文档进行比较, 只摘取跟文档有关系的放进数据库对应表格
            # 创建表 LinkInDoc 以及 domainid2urlindoc 的数据
            self.compare_db_data()

        # 访问数据库, 验证是否插入成功
        print("[*] 尝试访问数据库")
        assert len(LinkRelationShip.select().limit(10)) > 1
        assert len(DomainID2URL.select().limit(10)) > 1
        print("[*] 数据库中存在数据")

    def create_linkindoc_data(self, file_path):
        """
        经过处理创建 LinkInDoc 表格中的相关数据
        :param file_path:  str(), 文档文件的路径, 比如 "../news_tensite_xml.dat"
        :return: dict(), 域名及有效值, 比如 {"domain1": True, "domain2": False}
        """
        domain_dict = dict()

        for i, (domain_id, _) in enumerate(self.get_all_domain_id_in_doc(file_path)):
            if domain_id in domain_dict:
                continue

            result = LinkRelationShip.select().where(
                LinkRelationShip.page_id == domain_id or LinkRelationShip.out_id == domain_id
            ).execute()
            if result.count > 0:
                domain_dict[domain_id] = True
                print("[*] {} 找到了!目前是第 {} 个文档, 总共 1294233 个文档".format(domain_id, i + 1))
                for each_row in result:
                    # 如果链接相关的 2 个 id 都存在于 doc 中:
                    if (each_row.out_id not in self.doc_domain_id_url_dict) \
                            or (domain_id not in self.doc_domain_id_url_dict):
                        continue
                    # 如果是该网页被其他网页指向
                    elif each_row.out_id == domain_id:
                        LinkInDoc.insert({"domain_id": each_row.page_id, "out_id": domain_id}).execute()
                    # 如果是该网页指向其他网页
                    elif each_row.page_id == domain_id:
                        LinkInDoc.insert({"domain_id": domain_id, "out_id": each_row.out_id}).execute()
            else:
                domain_dict[domain_id] = False
                print("[-] {} 找不到!目前是第 {} 个文档, 总共 1294233 个文档".format(domain_id, i + 1))

        print("[*] 总共有域名 {} 个".format(len(domain_dict)))
        count_true, count_false = 0, 0
        for key, value in domain_dict.items():
            if value:
                print("[*] 找到有效域名: {}".format(key))
                count_true += 1
            else:
                count_false += 1
        print("[*] 有效域名: {} 个, 无效域名: {} 个".format(count_true, count_false))

        return domain_dict

    @staticmethod
    def _create_domainid2urlindoc_data(domain_dict):
        """
        【弃用】只把与有效域名相关的 URL 放进表格 domainid2urlindoc 中
        :param domain_dict: dict(), 域名及有效值, 比如 {"domain1": True, "domain2": False}
        :return: None
        """
        data_source = list()
        for each_domain, is_valid in domain_dict.items():
            if is_valid:
                result = DomainID2URL.select().where(DomainID2URL.page_id == each_domain).execute()
                for each_row in result:
                    data_source.append({"page_id": each_domain, "page_url": each_row.page_url})

        # 每隔 50 个数据插入一次:
        for i in range(0, len(data_source), 50):
            DomainID2URLInDoc.insert_many(data_source[i:i + 50]).execute()

    def compare_db_data(self):
        """
        将搜狗数据源的新闻数据与数据库中的数据相比较, 看有多少条匹配的信息在里头
        另外将比较的结果保存在表 LinkInDoc 里面
        结果是只有 6 个域名有匹配信息, 280 个域名没有匹配信息
        :return:
        """
        file_path = doc_file

        self.create_domain_id_2_url_in_doc_table_data()
        self.create_linkindoc_data(file_path)

    @staticmethod
    def first_way_to_check():
        try:
            LinkRelationShip.get(page_id="69713306c0bb3300")
            LinkRelationShip.get(page_id="49f37189a1acd500")
        except peewee.DoesNotExist:
            pass

    @staticmethod
    def second_way_to_check():
        test_1 = LinkRelationShip.select().where(LinkRelationShip.page_id == "69713306c0bb3300").execute()
        test_2 = LinkRelationShip.select().where(LinkRelationShip.page_id == "49f37189a1acd500").execute()

        for each in test_1:
            print(each.page_id)
            print(each.out_id)


class FakeDatabase(DatabaseBasicDeal):
    @staticmethod
    def compare_evaluate_doc_url(doc_domain_set):
        """
        匹配评估文件里面的 url 和 doc 里面存在的 url, 看是否能有合适的评估结果
        """
        evaluate_re = re.compile("\[(?P<keyword>.+)\]\s(?P<url>\S+)\s(?P<types>\d+)")
        reversed_dict = dict(zip(doc_domain_set.values(), doc_domain_set.keys()))

        with open(evaluate_file, "rt", encoding="gb18030", errors="ignore") as f:
            for each_line in f:
                re_result = evaluate_re.findall(each_line)
                if re_result:
                    keyword, url, search_type = re_result.pop()
                    sub_domain_url = extract_domain_from_url("http://{}".format(url))
                    if sub_domain_url in reversed_dict:
                        print("[*] 找到了: {}, {}, {}, {}".format(keyword, url,
                                                               search_type, reversed_dict[sub_domain_url]))

    @staticmethod
    def is_same_domain(url_x, url_y):
        """
        判断两个 URL 是不是属于同一个主域名
        主域名总共有五个:
            cn.yahoo.com
            people.com.cn
            news.ifeng.com
            news.163.com
            news.sohu.com
        :param url_x: str(), 比如: "cul.cn.yahoo.com"
        :param url_y: str(), 比如: "1688.news.cn.yahoo.com"
        :return: boolean(), 比如 True
        """
        main_domains = ["cn.yahoo.com", "people.com.cn", "news.ifeng.com", "news.163.com", "news.sohu.com"]
        for each_main in main_domains:
            if url_x.endswith(each_main) and url_y.endswith(each_main):
                return True
        return False

    @staticmethod
    def get_rates(domain_url):
        """
        根据 URL 给定不同的概率(三个概率分别代表: 不进行链接、外链、内链):
            cn.yahoo.com        ——      (60, 20, 20)
            people.com.cn       ——      (60, 10, 30)
            news.ifeng.com      ——      (60, 25, 15)
            news.163.com        ——      (60, 30, 10)
            news.sohu.com       ——      (60, 15, 25)
        :param domain_url: str(), 比如: "1688.news.cn.yahoo.com"
        :return: tuple, (int, int, int), 比如: (50, 25, 25)
        """
        domain_rates = {"cn.yahoo.com": (85, 7.5, 7.5),
                        "people.com.cn": (85, 4.25, 12.75),
                        "news.ifeng.com": (85, 10, 5),
                        "news.163.com": (85, 12.75, 4.25),
                        "news.sohu.com": (85, 5, 10)}
        for each_domain, rate in domain_rates.items():
            if domain_url.endswith(each_domain):
                return rate

    def create_fake_link_info(self, domain_info_dict):
        """
        创建伪造的链接信息
        :param domain_info_dict: dict(), 比如 {domain_id: domain_url, ...}
        :return: list(), 每一个元素是一条伪造的数据, (1, 2) 表示 1 指向 2, 比如 [(domain_id1, domain_id2),  ...]
        """
        link_result = list()
        for domain_x, url_x in domain_info_dict.items():
            for domain_y, url_y in domain_info_dict.items():
                # 获取概率指数
                rates = self.get_rates(url_x)
                choices = ["no", "out", "in"]

                # 随机选择一个: 【不链、外链、内链】
                choice = WeightRandom([(x, y) for x, y in zip(choices, rates)])()
                if choice == "no":
                    continue
                elif choice == "out" and not self.is_same_domain(url_x, url_y):
                    link_result.append((domain_x, domain_y))
                elif choice == "in" and self.is_same_domain(url_x, url_y):
                    link_result.append((domain_x, domain_y))

        return link_result

    def write_fake_link_into_db(self, link_result):
        """
        将伪造的数据写入到表 LinkInDoc 之中
        :param link_result:  list(), [(id1, id2), ...], 表示 id1 指向 id2
        :return: None, 直接写入到数据库
        """
        # 清除原来的数据
        self.clear_database([LinkInDoc])

        print("[*] 开始将数据写入到表 LinkInDoc 之中")
        data_list = list()
        for domain_id, out_id in link_result:
            data_list.append({"domain_id": domain_id, "out_id": out_id})

            if len(data_list) >= 400:
                LinkInDoc.insert_many(data_list).execute()
                del data_list[:]
        if len(data_list) >= 0:
            LinkInDoc.insert_many(data_list).execute()

    @staticmethod
    def analysis_fake_link_date(link_result, domain_info_dict):
        """
        统计链接的情况
        :param link_result: list(), 每一项是一条链接
        :param domain_info_dict: dict(), 域名与 url 的映射关系
        :return: None, 统计结果直接打印出来
        """
        inside_href = defaultdict(lambda: 0)
        outside_href = defaultdict(lambda: 0)
        main_domains = ["cn.yahoo.com", "people.com.cn", "news.ifeng.com", "news.163.com", "news.sohu.com"]

        for x, y in link_result:
            for each_main_domain in main_domains:
                if domain_info_dict[x].endswith(each_main_domain):
                    if x == y:
                        inside_href[each_main_domain] += 1
                    else:
                        outside_href[each_main_domain] += 1
                    break

        print("[*] 获得了 {} 条链接关系, 其中内联链接有 {} 条, 外链链接有 {} 条".format(
            len(link_result), sum(inside_href.values()), len(link_result) - sum(inside_href.values())))

        print("[*] 内联链接如下: ")
        for each_inside_href, count in inside_href.items():
            print("[*] {sep}{0}{sep2}->{sep2}{1} 条".format(each_inside_href, count, sep="\t", sep2="\t" * 3))

        print("[*] 外链链接情况如下: ")
        for each_outside_href, count in outside_href.items():
            print("[*] {sep}{0}{sep2}->{sep2}{1} 条".format(each_outside_href, count, sep="\t", sep2="\t" * 3))

    def run(self):
        """
        关系链接库只需要两个表:
            LinkInDoc: 用于存放链接关系, 即某个 id 被 某个 id 所指向之类的
            domainid2urlindoc: 将域名 id 转换为 url 的表
        :return:
        """
        # 创建 DomainID2URLInDoc 表, 运行一次即可, 没有数据才为这个表写数据
        if DomainID2URLInDoc.table_exists():
            if len(DomainID2URLInDoc.select()) == 0:
                self.create_domain_id_2_url_in_doc_table_data()
        else:
            DomainID2URLInDoc.create_table()
            self.create_domain_id_2_url_in_doc_table_data()

        domain_info_dict = self.get_all_domain_id_url_in_doc_from_db()

        # 创建评估数据
        self.compare_evaluate_doc_url(domain_info_dict)

        # 创建伪造的链接关系库
        self.clear_database([LinkInDoc])
        link_result = self.create_fake_link_info(domain_info_dict)
        self.analysis_fake_link_date(link_result, domain_info_dict)

        # 将伪造链接数据写入到数据库中
        print("[*] 开始将伪造的链接数据写入到数据库中")
        self.write_fake_link_into_db(link_result)


if __name__ == "__main__":
    # 自己伪造关系链接库
    fake_db = FakeDatabase()
    fake_db.run()

    # 根据搜狗提供的数据创建关系链接库
    # real_db = RealDatabase()
    # real_db.run()

    # 比较那个快一些
    # print(timeit.timeit("first_way_to_check()", "from __main__ import first_way_to_check", number=200))
    # print(timeit.timeit("second_way_to_check()", "from __main__ import second_way_to_check", number=200))
    pass
