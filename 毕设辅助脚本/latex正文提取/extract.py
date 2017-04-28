#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 自己写的论文是 LaTex 格式, 论文查重需要文本内容, 所以还是写个脚本来提取好了

2017.04.28 开始针对初始脚本进行提取, 针对 Windows 下生成的 tex 文件
"""
import os
import re

__author__ = '__L1n__w@tch'


class LatexExtract:
    @staticmethod
    def clear_tag(raw_data):
        """
        清除标签信息, \textbf{} 会保留花括号里面的内容, 不过 \label、\ref、\cite 就会删除花括号里面的内容
        :param raw_data: str(), 比如 "\\textbf{aaa}"
        :return: str(), "aaa"
        """

        def _sub_call(m):
            label = m.group(1)
            if label.lower() in ("label", "ref", "cite"):
                return str()
            else:
                return "{}".format(m.group(2))

        result = re.sub("\\\\(?P<label>.+?)\{(?P<content>.*)}", _sub_call, raw_data)
        return result

    @staticmethod
    def extract_content_from_label(segment):
        """
        label 标签啥都不匹配
        :param segment: str(), 比如 "\\label{chap:technology}"
        :return: str(), 比如 ""
        """
        return str()

    @staticmethod
    def extract_content_from_figure(segment):
        """
        从 figure 段中提取信息, 只提取 caption 信息
        :param segment: str(), 比如 "\\begin{figure}...\\end{figure}"
        :return: str(), 比如 "系统结构"
        """
        result = re.findall("\\\\caption{(.*)}", segment, flags=re.IGNORECASE)
        return result[0]

    def extract_content_from_itemize(self, segment):
        """
        提取 itemize 段, 例子参考 test 文件
        :param segment: str(), 比如 "\\begin{itemize}...\\end{itemize}"
        :return: str(), 比如 "各种供外部使用的~API~..."
        """
        result = re.findall("\\\\item\s(.*)", segment, flags=re.IGNORECASE)
        return "\n".join([self.clear_tag(x) for x in result])

    @staticmethod
    def get_types_from_begin(label_data):
        """
        提取 types 信息
        :param label_data: str(), 比如 "\\begin{figure}"
        :return: str(), 比如 "figure"
        """
        result = re.findall("\\\\begin\{(.*)}", label_data, flags=re.IGNORECASE)
        return result[0]

    def get_each_segment(self, raw_data):
        """
        实现分段操作
        :param raw_data: str(), 比如 "\\chapter{评测分析}\n\\section{实验环境}\n"
        :return: 生成器 yield 结果, 比如 ["\\chapter{评测分析}", "\\section{实验环境}"]
        """
        lines = iter(raw_data.split("\n"))
        each_line = next(lines, None)
        while each_line is not None:
            if r"\begin" in each_line:
                segment = list()

                types = self.get_types_from_begin(each_line)

                segment.append(each_line)
                # 迭代到 end 位置
                each_line = next(lines)
                while r"\end" not in each_line:
                    segment.append(each_line)
                    each_line = next(lines)
                segment.append(each_line)
                yield types, "\n".join(segment)

            # 如果是注释语句就忽略
            elif each_line.lstrip().startswith("%"):
                pass

            elif r"\label" in each_line:
                yield "label", each_line

            elif each_line != "":
                yield "text", each_line

            each_line = next(lines, None)

    def extract_content(self, content):
        """
        实现提取正文内容, 删除标签信息等
        :param content: str(), 比如 "\\chapter{评测分析}"
        :return: "评测分析\n"
        """
        result = list()

        for types, each_segment in self.get_each_segment(content):
            # 针对不同类型进行处理
            if types.lower() == "figure":
                result.append(self.extract_content_from_figure(each_segment))
            elif types.lower() == "itemize":
                result.append(self.extract_content_from_itemize(each_segment))
            elif types.lower() == "label":
                continue
            elif types.lower() == "Unknown":
                raise ("[-] 未知类型: {}".format(each_segment))
            else:
                result.append(each_segment)

        return "\n".join(self.clear_tag(x.replace("~", " ")) for x in result)

    def run(self, source_file_path):
        total_result = list()
        for each_file in ("chap-{}.tex".format(x) for x in ["intro", "tech", "implement", "analysis", "faq"]):
            with open(os.path.join(source_file_path, each_file), "rt", encoding="gb18030") as f:
                data = f.read()
                print("[*] 从 {file_name} 中提取内容完成".format(file_name=each_file))

                total_result.append(self.extract_content(data))
        print("[*] 所有内容提取完毕")
        return "\n\n".join(total_result)


if __name__ == "__main__":
    source_file_dir = "source_file"

    le = LatexExtract()
    result = le.run(source_file_dir)
    print(result)
