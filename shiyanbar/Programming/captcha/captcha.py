#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://www.shiyanbar.com/ctf/27
居然考到了验证码识别技术,网上搜了一大堆没搜到好库,跟着 writeup 自己手写一个算了
现在目前能做到的是识别正中间的验证码(使用第三方库实现)
'''
__author__ = '__L1n__w@tch'

from PIL import Image
import sys
import pyocr
import pyocr.builders
import pytesseract


def cut_noise(image):
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return image.point(table, '1')


def test(image_name):
    """
    只能识别验证码在正中间的情况
    :param image_name:
    :return:
    """
    with Image.open(image_name) as image:
        # 把彩色图像转化为灰度图像。彩色图像转化为灰度图像的方法很多，这里采用RBG转化到HSI彩色空间，采用L分量。
        image = image.convert("L")

        # 需要把图像中的噪声去除掉。这里的图像比较简单，直接阈值化就行了。我们把大于阈值threshold的像素置为1，其他的置为0。对此，先生成一张查找表，映射过程让库函数帮我们做。
        image = cut_noise(image)

        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("No OCR tool found")
            sys.exit(1)
        tool = tools[0]
        image.save("test.jpg")

        txt = tool.image_to_string(image, lang="eng", builder=pyocr.builders.TextBuilder())
        # Digits - Only Tesseract
        digits = tool.image_to_string(image, lang="eng", builder=pyocr.tesseract.DigitBuilder())
        print(txt)
        print(digits)


def test2(image_name):
    """
    只能识别验证码在中间的情况
    :param image_name:
    :return:
    """
    with Image.open(image_name) as image:
        image = image.convert("RGBA")
        pixdata = image.load()

        # Make the letters bolder for easier recognition
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                if pixdata[x, y][0] < 90:
                    pixdata[x, y] = (0, 0, 0, 255)

        for y in range(image.size[1]):
            for x in range(image.size[0]):
                if pixdata[x, y][1] < 136:
                    pixdata[x, y] = (0, 0, 0, 255)

        for y in range(image.size[1]):
            for x in range(image.size[0]):
                if pixdata[x, y][2] > 0:
                    pixdata[x, y] = (255, 255, 255, 255)

        # image.save("input-black.gif", "GIF")
        print(pytesseract.image_to_string(image))


def main():
    # test("test.png")
    test2("test.png")


if __name__ == "__main__":
    main()
