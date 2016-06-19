#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 写简历需要填 GPA, 西电好像没有 GPA 计算器, 那么我自己写一个好了

参考的 GPA 计算方式:
http://liuxue.xidian.edu.cn/info/1150/1438.htm
统一采取左边一列(虽然只影响评级好像)

平均绩点 = 所学课程学分绩之和 ÷ 所学课程学分数之和
一门课程的学分绩 = 绩点×学分数

百分制转换绩点对应表
90-100  4.0
85-89   3.7
82-84   3.3
78-81   3.0
75-77   2.7
72-74   2.3
69-71   2.0
66-68   1.7
63-65   1.5
60-62   1.0
59及以下 0.0

考查类课程三级计分成绩转换表
优秀  95  4.0
通过  80  3.0; 3.3
不通过    0.0

"免修" 课程计85分，绩点3.7

毕业设计等实践环节五级计分课程成绩转换表:
优   95  4.0
良   85  3.7
中   75  2.7; 3.0
及格  60  1.0
不及格     0.0
"""

__author__ = '__L1n__w@tch'


def get_score(score_file_name):
    """
    通过文件名得到对应的课程/成绩/学分, 存放进字典返回
    :param score_file_name: 记录成绩的文件名 "lf_score.txt"
    :return: {"线性代数":{"学分":"3", "成绩":"96"}}
    """
    score_dict = dict()
    with open(score_file_name, "r") as f:
        for each_line in f:
            if each_line.startswith("#"):
                continue  # 注释行
            each_line = each_line.strip()  # 清空换行符
            course_name, credit, score = each_line.split(" ")
            score_dict[course_name] = {"学分": credit, "成绩": score}

    return score_dict


def get_point(score):
    """
    将百分制成绩转换成对应的绩点
    :param score: 96
    :return: 4.0
    """
    if 90 <= score <= 100:
        point = 4.0
    elif 85 <= score <= 89:
        point = 3.7
    elif 82 <= score <= 84:
        point = 3.3
    elif 78 <= score <= 81:
        point = 3.0
    elif 75 <= score <= 77:
        point = 2.7
    elif 72 <= score <= 74:
        point = 2.4
    elif 69 <= score <= 71:
        point = 2.0
    elif 66 <= score <= 68:
        point = 1.7
    elif 63 <= score <= 65:
        point = 1.5
    elif 60 <= score <= 62:
        point = 1.0
    elif 0 <= score <= 59:
        point = 0.0
    else:
        raise ValueError("存在异常的分数")

    return point


def get_grade_point(data):
    """
    计算一门课程的学分绩
    :param data: {"学分":"3", "成绩":"96"}
    :return: 3, 3 * 4.0
    """
    credit = float(data["学分"])
    try:
        grade_point = credit * get_point(float(data["成绩"]))
    except ValueError:
        if data["成绩"] == "优秀":
            grade_point = credit * 4.0
        elif data["成绩"] == "通过":
            grade_point = credit * 3.0
        elif data["成绩"] == "不通过":
            grade_point = credit * 0.0
        else:
            raise RuntimeError("存在未定义学分绩转换公式")

    return credit, grade_point


def get_gpa(score_file_name):
    """
    通过文件中的数据计算得到 GPA
    :param score_file_name: 记录成绩的文件名 "lf_score.txt"
    :return: GPA 值, 比如 3.3
    """
    sum_grade_point = 0  # 学分绩之和
    sum_credit = 0  # 学分之和
    score = get_score(score_file_name)
    for each_course in score:
        # 获取每门课程的学分, 学分绩
        credit, grade_point = get_grade_point(score[each_course])
        sum_grade_point += grade_point
        sum_credit += credit
        print("课程名: {}, 学分: {}, 成绩: {}, 学分绩: {}".format(
            each_course, credit, score[each_course]["成绩"], grade_point))

    return sum_grade_point / sum_credit


if __name__ == "__main__":
    file_name = "lf_score.txt"
    gpa = get_gpa(file_name)
    print("GPA 成绩为: {}".format(gpa))
