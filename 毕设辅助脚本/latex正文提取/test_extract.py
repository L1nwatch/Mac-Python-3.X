#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 针对提取脚本作测试

2017.05.24 补充 cite 引证的相关测试
2017.05.20 补充关于提取图表时添加序号的测试
2017.05.19 添加提取摘要的相关代码实现
2017.05.18 补充数字与中文的转换, 还有添加序号的测试
2017.05.18 补充 item 中多个标签的获取测试, 其实是 clear tag 出了问题, 修复 math 测试的 BUG
2017.05.17 补充表格语法的提取测试
2017.05.11 修复在提取 $$ 语句时的 BUG
2017.05.10 补充 equation 标签的测试、以及 enumerate 的提取修复 BUG
2017.05.03 增加对 displaymath、lst input listing、$$ 等语法的处理的测试代码
"""
import unittest
from extract import LatexExtract

__author__ = '__L1n__w@tch'


class TestExtract(unittest.TestCase):
    def setUp(self):
        self.le = LatexExtract()

    def test_get_each_segment_can_del_with_table(self):
        test_data = r"""\begin{table}[htbp]
\caption{实验环境}
\label{tab:development_environment}
\centering
\begin{tabular}{c|l}
\hline
类别 & 内容 \\
\hline
处理器 & 2.9 GHz Intel Core i5 \\
内存 & 8~GB \\
操作系统 & OS X 10.10.5 \\
服务器 & Tomcatv7 \\
Lucene 版本 & Lucene~v4.3 \\
语言版本 & Python3、Java1.8 \\
\hline
\end{tabular}
\end{table}"""
        right_answer = [("table", test_data)]
        my_answer = self.le.get_each_segment(test_data)
        self.assertEqual(right_answer, list(my_answer))

    def test_extract_table(self):
        test_data = r"""\begin{table}[htbp]
\caption{实验环境}
\label{tab:development_environment}
\centering
\begin{tabular}{c|l}
\hline
类别 & 内容 \\
\hline
处理器 & 2.9 GHz Intel Core i5 \\
内存 & 8~GB \\
操作系统 & OS X 10.10.5 \\
服务器 & Tomcatv7 \\
Lucene 版本 & Lucene~v4.3 \\
语言版本 & Python3、Java1.8 \\
\hline
\end{tabular}
\end{table}"""
        self.le.chapter_level, self.le.table_level = 4, 0
        right_answer = "表 4.1 实验环境\n类别 & 内容\n处理器 & 2.9 GHz Intel Core i5\n内存 & 8~GB\n操作系统 & OS X 10.10.5\n服务器 & Tomcatv7\nLucene 版本 & Lucene~v4.3\n语言版本 & Python3、Java1.8"
        my_answer = self.le.extract_content_from_table(test_data)
        self.assertEqual(right_answer, my_answer)

    def test_extract_figure(self):
        """
        提取 figure 应该只提取 caption 字段
        :return:
        """
        test_data = r"""
\\begin{figure}[htbp]
\\centering
\\numberwithin{figure}{chapter}
\\includegraphics[width=0.7\textwidth]{figures/chap2/chap-2-system_lucene.png}
\\vspace{-1em}
\\caption{系统结构}
\\label{fig:lucene_system}
\\end{figure}"""
        self.le.chapter_level, self.le.figure_level = 1, 0
        right_answer = "图 1.1 系统结构"
        my_answer = self.le.extract_content_from_figure(test_data)
        self.assertEqual(right_answer, my_answer)

    def test_get_each_segment_can_deal_with_level(self):
        """
        测试能够添加标题序号
        """
        test_data = r"""\chapter{总结与展望}
\section{总结}
\subsection{aaa}
\subsubsection{bbb}
\section{展望}"""
        right_answer = [("chapter", "\chapter{总结与展望}"),
                        ("section", "\section{总结}"),
                        ("subsection", "\subsection{aaa}"),
                        ("subsubsection", "\subsubsection{bbb}"),
                        ("section", "\section{展望}")]
        my_answer = self.le.get_each_segment(test_data)
        self.assertEqual(right_answer, list(my_answer))

    def test_get_each_segment_can_work(self):
        """
        能够自动提取代码段, 比如说 figure 代码段
        :return:
        """
        test_data = """\chapter{相关技术和理论}\n\label{chap:technology}\n接下来介绍以下本文所涉及到的相关技术和理论知识，主要是搜索平台框架~Lucene~、针对中文的分词器、网页排序的算法介绍等。\n\section{Lucene~简介}"""
        right_answer = [("chapter", "\chapter{相关技术和理论}"), ("label", "\label{chap:technology}"),
                        ("text", "接下来介绍以下本文所涉及到的相关技术和理论知识，主要是搜索平台框架~Lucene~、针对中文的分词器、网页排序的算法介绍等。"),
                        ("section", "\section{Lucene~简介}")]
        my_answer = self.le.get_each_segment(test_data)
        self.assertEqual(right_answer, list(my_answer))

        test_data2 = r"""
\subsection{Lucene~介绍}

Lucene~是~Apache~Software~Foundation~的一个免费信息检索软件库\cite{lucene_introduce}。Lucene~提供了索引引擎以及查询引擎，以便支持全文检索功能。它使用了高度优化的倒排索引结构，并支持增量索引\cite{lucene_introduce2}，具有性能高、可扩展等特点。整个~Apache~的系统结构可以用下图 \ref{fig:lucene_system} 表示：

    \begin{figure}[htbp]
        \centering
        \numberwithin{figure}{chapter}
        \includegraphics[width=0.7\textwidth]{figures/chap2/chap-2-system_lucene.png}
        \vspace{-1em}
        \caption{系统结构}
        \label{fig:lucene_system}
    \end{figure}"""

        right_answer = [("subsection", "\subsection{Lucene~介绍}"),
                        ("text",
                         r"Lucene~是~Apache~Software~Foundation~的一个免费信息检索软件库\cite{lucene_introduce}。Lucene~提供了索引引擎以及查询引擎，以便支持全文检索功能。它使用了高度优化的倒排索引结构，并支持增量索引\cite{lucene_introduce2}，具有性能高、可扩展等特点。整个~Apache~的系统结构可以用下图 \ref{fig:lucene_system} 表示："),
                        ("figure",
                         "    \\begin{figure}[htbp]\n        \\centering\n        \\numberwithin{figure}{chapter}\n        \\includegraphics[width=0.7\\textwidth]{figures/chap2/chap-2-system_lucene.png}\n        \\vspace{-1em}\n        \\caption{系统结构}\n        \\label{fig:lucene_system}\n    \\end{figure}""")]
        my_answer = self.le.get_each_segment(test_data2)
        self.assertEqual(right_answer, list(my_answer))

    def test_get_each_segment_will_ignore_comment(self):
        """
        测试是否可以忽略注释
        :return:
        """
        test_data = '%部分用户开始倾向于使用专业化、领域化的搜索引擎，避免歧义的网页搜索结果。传统的搜索引擎还存在着不能即时更新网络信息资源的缺陷，在面对有即时性查询需求的用户搜索请求时，难免会不尽人意。'
        right_answer = []
        my_answer = self.le.get_each_segment(test_data)
        self.assertEqual(right_answer, list(my_answer))

    def test_extract_itemize(self):
        """
        验证提取 itemize 中的内容
        :return:
        """
        # 基本的 itemize 获取测试
        test_data = """
\\begin{itemize}
\\item \\textbf{各种供外部使用的~API~}：开发人员调用这些~API~可以进行搜索、分析，以及进一步对搜索结果进行处理等。
\\item \\textbf{基本包装结构}：主要是指内部使用的各种数据结构的封装，比如说每一个网页被封装成一个~document~数据结构等。
\\item \\textbf{索引核心}：主要提供为数据源建立特定的数据结构，即索引，这是~Lucene~优异检索性能的来源。生成的索引数据要在搜索时提供给对应接口，所以还涉及到存储相关的操作。
\\end{itemize}
"""
        right_answer = "\n".join(["各种供外部使用的~API~：开发人员调用这些~API~可以进行搜索、分析，以及进一步对搜索结果进行处理等。",
                                  "基本包装结构：主要是指内部使用的各种数据结构的封装，比如说每一个网页被封装成一个~document~数据结构等。",
                                  "索引核心：主要提供为数据源建立特定的数据结构，即索引，这是~Lucene~优异检索性能的来源。生成的索引数据要在搜索时提供给对应接口，所以还涉及到存储相关的操作。"])
        my_answer = self.le.extract_content_from_itemize(test_data)
        right_answer = right_answer.replace(" ", "").strip()
        my_answer = my_answer.replace(" ", "").strip()
        self.assertEqual(right_answer, my_answer)

        # 含换行符的 itemize 获取测试
        test_data = r"""\begin{enumerate}
  \item 互联网现状及搜索技术的了解学习

  ~~~~了解了互联网网站的发展趋势、有关互联网信息的几种检索方式、当前的互联网检索存在哪些难题需要攻克、用户对搜索结果的需求主要是哪些方面、国内外学者对搜索技术的关注度、搜索技术可以改进的方向及其改进成果等。

  \item 搜索技术的研究与实现

  ~~~~学习并掌握开源搜索框架~Lucene~的各个模块功能、内部机制及其接口调用、了解各个现有中文分词器优劣并实现、运用~B/S~架构结合相关编程语言搭建~Web~ 交互服务器，并最终搭建起了中文搜索平台。

  \item 网页排序算法的研究与实现

  ~~~~研究学习~4~种网页排序算法：基于传统~IR~的内容分析排序、基于发布者信息的排序、基于用户信息的排序、基于标注信息的排序；重点学习并实现了经典的基于超链分析的~HITS~以及~PageRank~排序算法。

  \item 检索性能的评测分析

  ~~~~了解信息检索领域常用的性能评价指标：平均准确率（MAP）、平均排序倒数（MRR）、准确率（Precision）、召回率（Recall）；学习使用~Selenium~框架模拟用户操作实现评估流程；采用~MRR~及~Precision~指标并根据评估数据对~HITS~以及~PageRank~进行评测分析对比。

\end{enumerate}"""
        right_answer = "\n\n".join([
            "互联网现状及搜索技术的了解学习\n\n~~~~了解了互联网网站的发展趋势、有关互联网信息的几种检索方式、当前的互联网检索存在哪些难题需要攻克、用户对搜索结果的需求主要是哪些方面、国内外学者对搜索技术的关注度、搜索技术可以改进的方向及其改进成果等。",
            "搜索技术的研究与实现\n\n~~~~学习并掌握开源搜索框架~Lucene~的各个模块功能、内部机制及其接口调用、了解各个现有中文分词器优劣并实现、运用~B/S~架构结合相关编程语言搭建~Web~ 交互服务器，并最终搭建起了中文搜索平台。",
            "网页排序算法的研究与实现\n\n~~~~研究学习~4~种网页排序算法：基于传统~IR~的内容分析排序、基于发布者信息的排序、基于用户信息的排序、基于标注信息的排序；重点学习并实现了经典的基于超链分析的~HITS~以及~PageRank~排序算法。",
            "检索性能的评测分析\n\n~~~~了解信息检索领域常用的性能评价指标：平均准确率（MAP）、平均排序倒数（MRR）、准确率（Precision）、召回率（Recall）；学习使用~Selenium~框架模拟用户操作实现评估流程；采用~MRR~及~Precision~指标并根据评估数据对~HITS~以及~PageRank~进行评测分析对比。"
        ])
        my_answer = self.le.extract_content_from_itemize(test_data)
        right_answer = right_answer.replace(" ", "").strip()
        my_answer = my_answer.replace(" ", "").strip()
        self.assertEqual(right_answer, my_answer)

        # item 中多个标签的获取测试
        test_data = r"""\begin{itemize}
  \item \textbf{基于字符串匹配的分词法}：亦称为机械分词或词典分词，按照一定的匹配规则对字符串进行扫描、匹配后进行切割，实现简单，但分词准确度不够；
  \item \textbf{基于统计学的分词法}：包括期望最大值算法、变长分词方法等，能够有效识别歧义与新词等，但需要大量训练；
  \item \textbf{机器学习分词法}：机器学习分词法主要有专家系统分词法和神经网络分词法等，可以智能学习，但实现难度较大。
\end{itemize}"""
        right_answer = "\n".join([
            "基于字符串匹配的分词法：亦称为机械分词或词典分词，按照一定的匹配规则对字符串进行扫描、匹配后进行切割，实现简单，但分词准确度不够；",
            "基于统计学的分词法：包括期望最大值算法、变长分词方法等，能够有效识别歧义与新词等，但需要大量训练；",
            "机器学习分词法：机器学习分词法主要有专家系统分词法和神经网络分词法等，可以智能学习，但实现难度较大。"
        ])
        my_answer = self.le.extract_content_from_itemize(test_data)
        right_answer = right_answer.replace(" ", "").strip()
        my_answer = my_answer.replace(" ", "").strip()
        self.assertEqual(right_answer, my_answer)

    def test_extract_label(self):
        """
        针对 label 则不进行提取操作
        :return:
        """
        test_data = "\\label{chap:technology}"
        right_answer = ""
        my_answer = self.le.extract_content_from_label(test_data)
        self.assertEqual(right_answer, my_answer)

    def test_clear_tag(self):
        test_data = "\\textbf{aa}"
        right_answer = "aa"
        my_answer = self.le.clear_tag(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = "bb\\textbf{aa}cc"
        right_answer = "bbaacc"
        my_answer = self.le.clear_tag(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = '当今互联网信息量正在持续地进行爆发性增长，网上资源的形式和内容也是日新月异。ILS（Internet~Live~Stats）组织致力于统计互联网的使用情况，图~\\ref{fig:internet_websites_count}~给出了自~1991~年以来网站数目的增长情况。'
        right_answer = "当今互联网信息量正在持续地进行爆发性增长，网上资源的形式和内容也是日新月异。ILS（Internet~Live~Stats）组织致力于统计互联网的使用情况，图~~给出了自~1991~年以来网站数目的增长情况。"
        my_answer = self.le.clear_tag(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = r'\ref{fig:internet_websites_count} '
        right_answer = " "
        my_answer = self.le.clear_tag(test_data)
        self.assertEqual(right_answer, my_answer)

        # 以下 3 个测试 cite 是否能够显示正确
        self.le.cite_list.clear()
        test_data = r'\cite{aaaa}'
        right_answer = "[1]"
        my_answer = self.le.clear_tag(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = r'\cite{bbbb}'
        right_answer = "[2]"
        my_answer = self.le.clear_tag(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = r'\cite{aaaa}'
        right_answer = "[1]"
        my_answer = self.le.clear_tag(test_data)
        self.assertEqual(right_answer, my_answer)
        self.assertEqual(["aaaa", "bbbb"], self.le.cite_list)

        test_data = "$a$"
        right_answer = "a"
        my_answer = self.le.clear_tag(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = r"$MAP = \frac{(1/1+2/3+3/5+4/7)}{50} \approx 0.06$"
        right_answer = r"MAP = (1/1+2/3+3/5+4/7)50  0.06"
        my_answer = self.le.clear_tag(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = r"$MAP = \frac{(1/2+2/4+3/6)}{50} = 0.03$"
        right_answer = r"MAP = (1/2+2/4+3/6)50 = 0.03"
        my_answer = self.le.clear_tag(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = r"$(0.06 + 0.03) / 2 \approx 0.05$"
        right_answer = r"(0.06 + 0.03) / 2  0.05"
        my_answer = self.le.clear_tag(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = r"\lstinputlisting{aaa}"
        right_answer = str()
        my_answer = self.le.clear_tag(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = r"\keywords{HITS，超链分析，网页排序，Lucene}"
        right_answer = "关键词：HITS，超链分析，网页排序，Lucene"
        my_answer = self.le.clear_tag(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = r"\englishkeywords{HITS, Hyperlink~Analysis, Web~Rank, Lucene}"
        right_answer = "Keywords:HITS, Hyperlink~Analysis, Web~Rank, Lucene"
        my_answer = self.le.clear_tag(test_data)
        self.assertEqual(right_answer, my_answer)

    def test_get_types_from_begin(self):
        test_data = "\\begin{figure}"
        right_answer = "figure"
        my_answer = self.le.get_types_from_begin(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = "\\begin{displaymath}"
        right_answer = "displaymath"
        my_answer = self.le.get_types_from_begin(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = "'\\begin{equation}\\label{eq:map}\n"
        right_answer = "equation"
        my_answer = self.le.get_types_from_begin(test_data)
        self.assertEqual(right_answer, my_answer)

    def test_add_order(self):
        """
        测试能够正确添加序号
        """
        self.le.chapter_level = 0
        test_data = r"\chapter{总结与展望}"
        right_answer = "第一章 总结与展望"
        my_answer = self.le.add_order(test_data, "chapter")
        self.assertEqual(right_answer, my_answer)

        self.le.chapter_level, self.le.section_level = 1, 0
        test_data = r"\section{总结与展望}"
        right_answer = "1.1 总结与展望"
        my_answer = self.le.add_order(test_data, "section")
        self.assertEqual(right_answer, my_answer)

        self.le.chapter_level, self.le.section_level, self.subsection_level = 1, 1, 0
        test_data = r"\subsection{总结与展望}"
        right_answer = "1.1.1 总结与展望"
        my_answer = self.le.add_order(test_data, "subsection")
        self.assertEqual(right_answer, my_answer)

        self.le.chapter_level, self.le.section_level, self.subsection_level, self.subsubsection_level = 1, 1, 1, 0
        test_data = r"\subsubsection{总结与展望}"
        right_answer = "1.1.1.1 总结与展望"
        my_answer = self.le.add_order(test_data, "subsubsection")
        self.assertEqual(right_answer, my_answer)

    def test_add_order_can_reset(self):
        """
        当进入下一个章节时, section 等的序号应该清空, 这里编写代码进行对应测试
        """
        self.le.chapter_level = 0
        test_data = r"\chapter{总结与展望}"
        right_answer = "第一章 总结与展望"
        my_answer = self.le.add_order(test_data, "chapter")
        self.assertEqual(right_answer, my_answer)

        self.le.section_level = 0
        test_data = r"\section{总结与展望}"
        right_answer = "1.1 总结与展望"
        my_answer = self.le.add_order(test_data, "section")
        self.assertEqual(right_answer, my_answer)

        self.le.subsection_level = 0
        test_data = r"\subsection{总结与展望}"
        right_answer = "1.1.1 总结与展望"
        my_answer = self.le.add_order(test_data, "subsection")
        self.assertEqual(right_answer, my_answer)

        self.le.subsubsection_level = 0
        test_data = r"\subsubsection{总结与展望}"
        right_answer = "1.1.1.1 总结与展望"
        my_answer = self.le.add_order(test_data, "subsubsection")
        self.assertEqual(right_answer, my_answer)

        test_data = r"\section{总结与展望}"
        right_answer = "1.2 总结与展望"
        my_answer = self.le.add_order(test_data, "section")
        self.assertEqual(right_answer, my_answer)

        test_data = r"\subsection{总结与展望}"
        right_answer = "1.2.1 总结与展望"
        my_answer = self.le.add_order(test_data, "subsection")
        self.assertEqual(right_answer, my_answer)

        test_data = r"\subsubsection{总结与展望}"
        right_answer = "1.2.1.1 总结与展望"
        my_answer = self.le.add_order(test_data, "subsubsection")
        self.assertEqual(right_answer, my_answer)

        test_data = r"\chapter{总结与展望}"
        right_answer = "第二章 总结与展望"
        my_answer = self.le.add_order(test_data, "chapter")
        self.assertEqual(right_answer, my_answer)

    def test_covert_number_to_chinese(self):
        right_answer = ["一", "二", "三", "四", "五"]
        for i in range(1, len(right_answer) + 1):
            self.assertEqual(right_answer[i - 1], self.le.covert_number_to_chinese(i))

    def test_extract_content_from_abstract(self):
        """
        测试从摘要提取内容
        """
        test_data = r"""\begin{abstract}

当今互联网信息量正在持续地进行爆发性增长，用户在使用~Web~搜索引擎查找所需信息时，经常发现检索结果太过冗余，往往需要人工过滤才能得到想要的信息。目前用户的需求已经不是获取更多的信息，而是想要获取更加精确、有质量的搜索结果。而基于超链分析的网页排序算法，能够在一定程度上避免手工操作，帮用户过滤掉无用的搜索结果。因此，基于超链分析的网页排序算法是信息检索领域中人们重点关注的方向之一。

本文对互联网现状、互联网网站的发展趋势，以及搜索技术比如搜索方式、搜索难题、网页排序算法等进行了了解和学习。考虑到超链分析在互联网搜索这一领域中所具有的特殊地位，本文重点研究了~HITS~算法并在现有开源框架~Lucene~上搭建了中文搜索平台，将这一网页排序算法嵌入到检索流程之中，同时进行了评测工作，通过平均排序倒数（MRR）以及查准率（Precision）指标，与~PageRank~排序算法进行对比，研究~HITS~网页排序算法所存在的缺陷与不足之处，并学习及探讨其改进方向及现有改进成果。

通过分析互联网中真实的超链接数据信息，发现了许多网站存在内联链接、竞争对手之间很少进行相互链接等情况。经过实验表明，虽然~HITS、PageRank~算法弥补了全文检索无法搜索到不包含关键词的好页面这一不足之处，但它们均容易受到恶意链接的干扰，导致网页排名不公平。通过观察评测结果，发现当内链数目较多时，~HITS~算法在实验中的表现要优于~PageRank~算法；而当外链数目较多时，~PageRank~算法的表现要优于~HITS~算法。

\keywords{HITS，超链分析，网页排序，Lucene}
\end{abstract}
"""
        right_answer = r"""摘要

当今互联网信息量正在持续地进行爆发性增长，用户在使用~Web~搜索引擎查找所需信息时，经常发现检索结果太过冗余，往往需要人工过滤才能得到想要的信息。目前用户的需求已经不是获取更多的信息，而是想要获取更加精确、有质量的搜索结果。而基于超链分析的网页排序算法，能够在一定程度上避免手工操作，帮用户过滤掉无用的搜索结果。因此，基于超链分析的网页排序算法是信息检索领域中人们重点关注的方向之一。

本文对互联网现状、互联网网站的发展趋势，以及搜索技术比如搜索方式、搜索难题、网页排序算法等进行了了解和学习。考虑到超链分析在互联网搜索这一领域中所具有的特殊地位，本文重点研究了~HITS~算法并在现有开源框架~Lucene~上搭建了中文搜索平台，将这一网页排序算法嵌入到检索流程之中，同时进行了评测工作，通过平均排序倒数（MRR）以及查准率（Precision）指标，与~PageRank~排序算法进行对比，研究~HITS~网页排序算法所存在的缺陷与不足之处，并学习及探讨其改进方向及现有改进成果。

通过分析互联网中真实的超链接数据信息，发现了许多网站存在内联链接、竞争对手之间很少进行相互链接等情况。经过实验表明，虽然~HITS、PageRank~算法弥补了全文检索无法搜索到不包含关键词的好页面这一不足之处，但它们均容易受到恶意链接的干扰，导致网页排名不公平。通过观察评测结果，发现当内链数目较多时，~HITS~算法在实验中的表现要优于~PageRank~算法；而当外链数目较多时，~PageRank~算法的表现要优于~HITS~算法。

\keywords{HITS，超链分析，网页排序，Lucene}

"""
        my_answer = self.le.extract_content_from_abstract(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = r"""\begin{englishabstract}
\englishkeywords{HITS, Hyperlink~Analysis, Web~Rank, Lucene}
\end{abstract}
"""
        right_answer = r"""ABSTRACT
\englishkeywords{HITS, Hyperlink~Analysis, Web~Rank, Lucene}

"""
        my_answer = self.le.extract_content_from_abstract(test_data)
        self.assertEqual(right_answer, my_answer)


if __name__ == "__main__":
    pass
