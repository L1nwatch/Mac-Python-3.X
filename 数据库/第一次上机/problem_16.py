#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 不太确定自己的结果是否是正确的, 只好通过 Python 来验证一下了, 反正就一道题

查询有4门以上课程是92分以上的学生的学号及(90分以上的)课程数
'''
__author__ = '__L1n__w@tch'


class Student:
    def __init__(self, student_number):
        self.student_number = student_number
        self.course_score = dict()

    def print_info(self):
        print("My student number is {}".format(self.student_number))
        for each_course in self.course_score:
            print("Course number {} {} Course score {}".format(each_course, "-" * 10, self.course_score[each_course]))


def create_db():
    students = dict()

    with open("sc.txt", "r") as f:
        for each_line in f:
            student_number, course_number, student_score = [x.strip() for x in each_line.split(",")]
            if student_number not in students:
                students[student_number] = Student(student_number)
            students[student_number].course_score[course_number] = student_score

    return students


if __name__ == "__main__":
    students = create_db()

    for student in students:
        counts = 0
        for each_course in students[student].course_score:
            if int(students[student].course_score[each_course]) > 92:
                counts += 1
        if counts > 4:
            students[student].print_info()
