#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 尝试使用 selenium 进行评测工作

2017.04.07 开始使用 selenium 库进行评测相关的自动化操作
"""
import unittest
import fractions

from selenium.webdriver import Firefox

__author__ = '__L1n__w@tch'

need_test = False


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
        for right_answer, my_answer in zip(right_results, page_rank_results):
            self.assertEqual(my_answer.text, right_answer)

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
        for right_answer, my_answer in zip(right_results, hits_results):
            self.assertEqual(my_answer.text, right_answer)

    @staticmethod
    def index_in_list_text(a_list, content):
        for i, each in enumerate(a_list):
            if content == each.text:
                return i

    def test_mrr_algorithm(self):
        """
        这不是测试, 而是进行 mrr 的计算, 只不过得以 test 开头才能运行(或者说我懒得研究其他运行方式- -)
        MRR: 平均排序倒数(MRR, Mean Reciprocal Rank of Homepage), 即对每个问题而言,
             把标准答案在被评价系统给出结果中的排序取倒数作为它的准确度, 再对所有的问题取平均
        """
        keyword_result_dict = {
            "test": "某个被搜索结果指向的页面",
            "life": "新加坡华人任证婚人7年 见证781对情侣缔结良缘",
        }
        hits_mrr_result = list()
        page_rank_mrr_result = list()

        for each_keyword, each_related in keyword_result_dict.items():
            # 进行 HITS 的 MRR 计算
            self.do_search(each_keyword)
            hits_results = self.browser.find_elements_by_id("id_hits_result")
            hits_mrr_result.append(
                fractions.Fraction(1, self.index_in_list_text(hits_results, each_related) + 1)
            )

            # 进行 PageRank 的 MRR 计算
            page_rank_results = self.browser.find_elements_by_id("id_page_rank_result")
            page_rank_mrr_result.append(
                fractions.Fraction(1, self.index_in_list_text(page_rank_results, each_related) + 1)
            )

        print("[*] 最终计算 HITS 的 MRR 为: {}".format(sum(hits_mrr_result) / len(hits_mrr_result)))
        print("[*] 最终计算 PageRank 的 MRR 为: {}".format(sum(page_rank_mrr_result) / len(page_rank_mrr_result)))


if __name__ == "__main__":
    pass
