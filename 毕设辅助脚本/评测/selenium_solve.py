#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 尝试使用 selenium 进行评测工作

2017.05.06 修改评测的测试代码, 使其兼容最新的链接关系库
2017.04.08 补充完成 precision 的计算工作
2017.04.07 开始使用 selenium 库进行评测相关的自动化操作
"""
import unittest
import fractions

from selenium.webdriver import Firefox

__author__ = '__L1n__w@tch'

need_test = False
mrr_test_data = {
    "张筱雨": "news.163.com",
    "接吻技巧": "life.people.com.cn",
    "美女走光": "news.163.com",
    "作爱": "news.sohu.com",
    "一本道": "news.sohu.com",
    "我淫我色": ["hi.people.com.cn", "media.people.com.cn"],
    "春节放假通知": "news.sohu.com",
    "成人图片": "news.sohu.com",
    "电信重组": "it.people.com.cn",
    "陈良宇": "news.ifeng.com",
    "做爱图片": ["pic.people.com.cn", "news.sohu.com", "news.163.com", "pic.people.com.cn"],
    "璩美凤": "news.sohu.com",
    "情色小说": "news.sohu.com",
    "美国大选": "news.ifeng.com",
    "mm美图": ["news.163.com", "it.people.com.cn"],
    "春节放假": "news.sohu.com",
    "人民网": "www.people.com.cn",
    "色情电影": "www.people.com.cn",
    "台湾新闻": "news.ifeng.com",
    "99bb": "news.sohu.com",
    "大雪无情人有情": "tv.people.com.cn",
    "南方雪灾": "news.sohu.com",
    "朝鲜": "news.sohu.com",
    "法定节假日": "news.sohu.com",
    "婚姻法": "www.people.com.cn",
    "人民日报": "www.people.com.cn",
    "激情": ["health.people.com.cn", "pic.people.com.cn"],
    "赵紫阳": "cpc.people.com.cn",
}
precision_test_data = mrr_test_data


class AnalysisTest(unittest.TestCase):
    def setUp(self):
        self.home_url = "localhost:8080"
        self.browser = Firefox()
        self.browser.implicitly_wait(5)

    def do_search(self, keyword):
        self.browser.get(self.home_url)
        search_button = self.browser.find_element_by_id("search")
        search_button.send_keys("{}\n".format(keyword))

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    @unittest.skipUnless(need_test, "need_test 为 True 时才进行测试")
    def test_open_home(self):
        """
        测试能够打开 Home 页面
        """
        self.browser.get(self.home_url)
        self.assertIn("w@tch", self.browser.page_source)

    @unittest.skipUnless(need_test, "need_test 为 True 时才进行测试")
    def test_can_search(self):
        """
        测试能够进行搜索
        """
        self.do_search("test")
        self.assertIn("PageRank", self.browser.page_source)

    @unittest.skipUnless(need_test, "need_test 为 True 时才进行测试")
    def test_can_get_all_pagerank_result(self):
        """
        测试能够获取所有的 pagerank 排序结果
        """
        self.do_search("test")
        page_rank_results = self.browser.find_elements_by_id("id_page_rank_result")
        right_results = ["通过启德内部英文测试澳洲14所院校可免雅思",
                         "法国强制司机购买酒精测试仪 新规被批假公济私",
                         "英配偶签证保证人最低年收入调整为18600英镑",
                         "某个被搜索结果指向的页面",
                         "某个被搜索结果指向的页面",
                         "某个被搜索结果指向的页面",
                         "某个被搜索结果指向的页面",
                         "某个被搜索结果指向的页面",
                         "某个被搜索结果指向的页面",
                         "某个被搜索结果指向的页面",
                         'DotA2每周更新:test版新增大魔导师',
                         'DotA2每周更新:test版新增大魔导师',
                         '新西兰KIWI出口商对中国制造商说“NO”',
                         'Major headlines',
                         "People's Daily Online",
                         "People's Daily Online",
                         "People's Daily Online",
                         "People's Daily Online",
                         "网友咨询河南省公务员报考情况",
                         "法国强制司机购酒精测试仪并随身携带 自驾游客不例外"]
        my_results = [my_answer.text for my_answer in page_rank_results]
        self.assertTrue(any(
            [right_answer in my_results for right_answer in right_results]
        ))

    @unittest.skipUnless(need_test, "need_test 为 True 时才进行测试")
    def test_can_get_all_hits_result(self):
        """
        测试能够获取所有的 hits 排序结果
        """
        self.do_search("test")
        hits_results = self.browser.find_elements_by_id("id_hits_result")
        right_results = ["通过启德内部英文测试澳洲14所院校可免雅思",
                         "法国强制司机购买酒精测试仪 新规被批假公济私",
                         "英配偶签证保证人最低年收入调整为18600英镑",
                         "某个被搜索结果指向的页面",
                         "某个被搜索结果指向的页面",
                         "某个被搜索结果指向的页面",
                         "某个被搜索结果指向的页面",
                         "某个被搜索结果指向的页面",
                         "某个被搜索结果指向的页面",
                         "某个被搜索结果指向的页面",
                         "DotA2每周更新:test版新增大魔导师",
                         "DotA2每周更新:test版新增大魔导师",
                         "新西兰KIWI出口商对中国制造商说“NO”",
                         "Major headlines",
                         "People's Daily Online",
                         "People's Daily Online",
                         "People's Daily Online",
                         "People's Daily Online",
                         "网友咨询河南省公务员报考情况",
                         "法国强制司机购酒精测试仪并随身携带 自驾游客不例外"]
        my_results = [my_answer.text for my_answer in hits_results]
        self.assertTrue(any(
            [right_answer in my_results for right_answer in right_results]
        ))

    @staticmethod
    def index_in_list_text(a_list, content):
        for i, each in enumerate(a_list):
            if isinstance(content, list):
                for each_content in content:
                    if each_content in each.text:
                        return i
            elif content in each.text:
                return i

    @staticmethod
    def get_evaluate_main_domain(evaluate_sub_domain):
        """
        根据给定的子域名, 求出用来评估的主域名
        :param evaluate_sub_domain: list() or str(), 用于评估的相关结果
        :return: set(), 每一个元素是用来评估的主要域名
        """
        main_domains = ["cn.yahoo.com", "people.com.cn", "news.ifeng.com", "news.163.com", "news.sohu.com"]
        evaluate_domain = set()

        # 找出哪个是要用于评估的主要域名
        for each_main_domain in main_domains:
            if isinstance(evaluate_sub_domain, list):
                for each_sub_domain in evaluate_sub_domain:
                    if each_sub_domain.endswith(each_main_domain):
                        evaluate_domain.add(each_main_domain)
            elif str(evaluate_sub_domain).endswith(each_main_domain):
                evaluate_domain.add(each_main_domain)

        return evaluate_domain

    def count_related_in_list_text(self, a_list, evaluate_sub_domain):
        """
        辅助 Precision 计算用的, 用于统计搜索结果中有多少个是相关结果
        :param a_list: list(), 搜索结果
        :param evaluate_sub_domain: list() or str(), 用于评估的相关结果
        :return: int(), 相关结果个数
        """
        evaluate_domain = self.get_evaluate_main_domain(evaluate_sub_domain)

        count = 0
        for each_result in a_list:
            for each_main_domain in evaluate_domain:
                if each_main_domain in each_result.text:
                    count += 1
        return count

    @unittest.skipUnless(True, "要进行 MRR 计算的话才改为 True")
    def test_mrr_algorithm(self):
        """
        这不是测试, 而是进行 mrr 的计算, 只不过得以 test 开头才能运行(或者说我懒得研究其他运行方式- -)
        MRR: 平均排序倒数(MRR, Mean Reciprocal Rank of Homepage), 即对每个问题而言,
             把标准答案在被评价系统给出结果中的排序取倒数作为它的准确度, 再对所有的问题取平均
        """
        keyword_result_dict = mrr_test_data
        hits_mrr_result = list()
        page_rank_mrr_result = list()

        print("\n[*] {sep} 以下进行 MRR 计算 {sep}".format(sep="=" * 30))
        for each_keyword, evaluate_domain in keyword_result_dict.items():
            # 进行 HITS 的 MRR 计算
            self.do_search(each_keyword)
            hits_results = self.browser.find_elements_by_id("id_hits_result")
            try:
                hits_mrr_result.append(
                    fractions.Fraction(1, self.index_in_list_text(hits_results, evaluate_domain) + 1)
                )
                print("[*] 找到词汇: {}, MRR 评分为: {}".format(each_keyword, hits_mrr_result[-1]))
            except TypeError as e:
                print("[-] 词汇找不到结果: {}".format(each_keyword))
                continue

            # 进行 PageRank 的 MRR 计算
            page_rank_results = self.browser.find_elements_by_id("id_page_rank_result")
            page_rank_mrr_result.append(
                fractions.Fraction(1, self.index_in_list_text(page_rank_results, evaluate_domain) + 1)
            )

        print("[*] 最终计算 HITS 的 MRR 为: {}".format(sum(hits_mrr_result) / len(hits_mrr_result)))
        print("[*] 最终计算 PageRank 的 MRR 为: {}".format(sum(page_rank_mrr_result) / len(page_rank_mrr_result)))

    @unittest.skipUnless(True, "要进行查准率(precision)计算的话才改为 True")
    def test_precision_algorithm(self):
        """
        这不是测试, 而是进行查准率计算
        precision: 实验中对返回结果的前 20 项进行评测, 设与查询问题 i 相关的结果个数为 ni, 则该次查询的查准率 Pi = ni / 20,
                   再对所有查询取平均值
        """
        keyword_result_dict = precision_test_data
        hits_precision_result = list()
        pagerank_precision_result = list()

        print("\n[*] {sep} 以下进行 precision 计算 {sep}".format(sep="=" * 30))
        # 遍历每一个查询
        for each_keyword, each_related in keyword_result_dict.items():
            # 进行 HITS 的 Precision 计算
            self.do_search(each_keyword)
            hits_results = self.browser.find_elements_by_id("id_hits_result")
            # 对 HITS 计算 ni / 20, 保存下来
            hits_precision_result.append(
                fractions.Fraction(self.count_related_in_list_text(hits_results, each_related), len(hits_results))
            )

            # 进行 PageRank 的 Precision 计算
            pagerank_results = self.browser.find_elements_by_id("id_page_rank_result")
            # 对 PageRank 计算 ni / 20, 保存下来
            pagerank_precision_result.append(
                fractions.Fraction(
                    self.count_related_in_list_text(pagerank_results, each_related), len(pagerank_results)
                )
            )
            print("[*] 针对 '{}', HITS 匹配 {}, PageRank 匹配 {}".format(each_keyword,
                                                                   hits_precision_result[-1],
                                                                   pagerank_precision_result[-1]))

        # 进行 P 值计算
        print("[*] 最终计算 HITS 的 Precision 为: {}".format(sum(hits_precision_result) / len(hits_precision_result)))
        print("[*] 最终计算 PageRank 的 Precision 为: {}".format(
            sum(pagerank_precision_result) / len(pagerank_precision_result))
        )


if __name__ == "__main__":
    pass
