#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 自己写的论文是 LaTex 格式, 论文查重需要文本内容, 所以还是写个脚本来提取好了

2017.05.18 修复 clear tag 的一个 BUG
2017.05.17 补充提取表格语句的相关代码实现
2017.05.11 修复在提取 $$ 语句时的 BUG
2017.05.10 补充 equation 标签的过滤、以及针对 itemize 和 enumerate 的提取修复 BUG
2017.05.03 增加对 displaymath、lst input listing、$$ 等语法的处理
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
            if label.lower() in ("label", "ref", "cite", "lstinputlisting"):
                return str()
            else:
                return "{}".format(m.group(2))

        def _math_clean(m):
            content = m.group(1)

            content = content.replace("\approx", "")
            content = re.sub("\\f.*?{(?P<save>.+?)}", "\g<save>", content)
            content = re.sub("{(?P<save>.+?)}", "\g<save>", content)

            return content

        clean_data = re.sub("\$(?P<content>.+?)\$", _math_clean, raw_data)
        clean_data = re.sub("\\\\(?P<label>.+?)\{(?P<content>.*?)\}", _sub_call, clean_data)

        return clean_data

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
        re_result = re.findall("\\\\caption{(.*)}", segment, flags=re.IGNORECASE)
        return re_result[0]

    def extract_content_from_itemize(self, segment):
        """
        提取 itemize 段, 例子参考 test 文件
        :param segment: str(), 比如 "\\begin{itemize}...\\end{itemize}"
        :return: str(), 比如 "各种供外部使用的~API~..."
        """
        # 删除 begin end 标签
        re_result = re.findall("\\\\begin{[^}]+}(.+)\\\\end{.+}", segment, flags=re.IGNORECASE | re.DOTALL)[0]
        # 删除 item 标签
        re_result = re_result.replace("\\item", "")
        return self.clear_tag(re_result)

    @staticmethod
    def get_types_from_begin(label_data):
        """
        提取 types 信息
        :param label_data: str(), 比如 "\\begin{figure}"
        :return: str(), 比如 "figure"
        """
        re_result = re.findall("\\\\begin\{(.*?)}.*", label_data, flags=re.IGNORECASE)
        return re_result[0]

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
                while not each_line.lstrip().startswith(r"\end{{{}}}".format(types)):
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

    def extract_content_from_table(self, segment):
        """
        提取 table 字段的内容, 例子参考 test 文件
        :param segment: str(), 比如 "\begin{table}[htbp]...\end{tabular}"
        :return: str(), 表格里面的所有内容
        """
        result = list()
        for each_line in segment.splitlines():
            if each_line.lstrip().startswith(r"\caption"):
                result.append(self.clear_tag(each_line))
            elif each_line.endswith(r"\\"):
                result.append(each_line.strip(r" \\"))
        return "\n".join(result)

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
            elif types.lower() in ("itemize", "enumerate"):
                result.append(self.extract_content_from_itemize(each_segment))
            elif types.lower() in ("label", "displaymath", "equation"):
                continue
            elif types.lower() == "table":
                result.append(self.extract_content_from_table(each_segment))
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
        print("[*] 所有内容提取完毕, 总共 {} 字".format(sum(len(x) for x in total_result)))
        return "\n\n\n".join(total_result)


if __name__ == "__main__":
    source_file_dir = "source_file"

    le = LatexExtract()
    full_text = le.run(source_file_dir)
    with open("final_result.txt", "wt") as result_file_io:
        result_file_io.write(full_text)
