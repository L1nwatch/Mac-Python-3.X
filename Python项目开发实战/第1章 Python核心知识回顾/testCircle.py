# -*- coding: utf-8 -*-
# version: Python3.X
__author__ = '__L1n__w@tch'

import math


class Circle:
    def __init__(self, radius):
        """
        强制用户使用set_radius()方法修改半径值, 通过在特性self.__radius前面加上双下划线前缀实现这一点, 这是Python所用的私有化方法
        :param radius:
        :return:
        """
        self.__radius = radius

    def set_radius(self, new_value):
        if new_value >= 0:
            self.__radius = new_value
        else:
            raise ValueError("Value must be positive")

    def area(self):
        return math.pi * (self.__radius ** 2)


class Circle2:
    def __init__(self, radius):
        self.__radius = radius

    def __set_radius(self, new_value):
        if new_value >= 0:
            self.__radius = new_value
        else:
            raise ValueError("Value must be positive")

    # 创建一个只写特性radius
    # 这行代码接受的参数是一组函数, 它们用来执行读、写和删除操作(以及文档字符串)
    # 每个函数的默认值都是None,这里设置读函数为None,写函数为__set_radius方法
    # 这样做的结果是: 用户可以吧它当成一个公共的数据特性访问,但是当给其赋值时,就必须调用__set_radius()方法来保护这个值
    # 任何试图读取(或删除)这个特性的操作都会被忽略,因为这些操作实际上操作的都是None
    radius = property(None, __set_radius)

    # area属性使用了Python属性修饰符(@property),属性修饰符是一种创建只读属性的快捷方式
    @property
    def area(self):
        return math.pi * (self.__radius ** 2)


def main():
    c1 = Circle(42)
    print(c1.area())
    try:
        print(c1.__radius)
    except AttributeError as e:
        print("try c1.__radius: ", e)
    c1.set_radius(66)
    print(c1.area())
    try:
        c1.set_radius(-4)
    except ValueError as e:
        print("try c1.set_radius(-4): ", e)

    c2 = Circle2(42)
    print(c2.area)
    try:
        print(c2.radius)
    except AttributeError as e:
        print("try print(c2.radius): ", e)
    c2.radius = 12
    print(c2.area)
    try:
        c2.radius = -4
    except ValueError as e:
        print("try c2.radius = -4: ", e)


if __name__ == "__main__":
    main()
