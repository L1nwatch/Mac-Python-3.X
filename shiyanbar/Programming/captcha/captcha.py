#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://www.shiyanbar.com/ctf/27
居然考到了验证码识别技术,网上搜了一大堆没搜到好库,跟着 writeup 自己手写一个算了
现在目前能做到的是识别正中间的验证码(使用第三方库实现)
'''
__author__ = '__L1n__w@tch'

from PIL import Image
import pyocr
import pyocr.builders
import pytesseract
import os


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


def create_pix_tables(image):
    """
    把图像的每个点都保存到列表中
    :param image:
    :return:
    """
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    result = list()
    for x in range(width):
        for y in range(height):
            result.append(pix[x, y])
    return result


def convert_black_white(image):
    """
    对图片进行黑白处理
    :param image:
    :return:
    """
    image = image.convert("L")
    WHITE, BLACK = 255, 0
    image = image.point(lambda x: WHITE if x >= 230 else BLACK)
    image = image.convert('1')
    return image


def get_font():
    """
    获取提前提取好的每个数字的图片
    :return:
    """
    font = []
    path = "font"

    for i in range(10):
        with Image.open(path + os.sep + str(i) + ".bmp") as image:
            font.append(create_pix_tables(convert_black_white(image)))
    return font


def cut(image):
    """
    把 4 个数字区分出来,注意前 2 个坐标是左上角坐标, 后 2 个坐标是右下角坐标
    :param image:
    :return:
    """
    box1 = (0, 0, 6, 10)
    box2 = (10, 0, 16, 10)
    box3 = (20, 0, 26, 10)
    box4 = (30, 0, 36, 10)
    im1 = image.crop(box1)
    im2 = image.crop(box2)
    im3 = image.crop(box3)
    im4 = image.crop(box4)
    return im1, im2, im3, im4


def image_to_string(image):
    """
    识别出一张图片里面的 4 个数字
    :param image:
    :return:
    """
    global font
    test1 = convert_black_white(image)
    text = str()
    for each in cut(test1):
        for num in range(10):
            if create_pix_tables(each) == font[num]:
                text += str(num)
                break
    return text


def solve():
    """
    参考 WP 写的, 原理就是自己手动取出每一个数字的图像, 然后再依次进行比较
    :return:
    """
    global font
    font = get_font()
    path = "/Users/L1n/Desktop/bmp"
    sum = 0
    for i in range(1, 10000):
        with Image.open(path + os.sep + str(i) + ".bmp") as image:
            sum += i * int(image_to_string(image))
    print("Sum: {}".format(sum))


def main():
    # test("1.png")
    # test2("1.png")
    solve()


if __name__ == "__main__":
    main()
