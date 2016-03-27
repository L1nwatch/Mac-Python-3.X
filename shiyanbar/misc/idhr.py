#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' url: http://www.shiyanbar.com/ctf/1832
主要学习 png 头的相关知识点

png格式主要由六大块组成：文件头、IHDR块、PLTE块、tRNS块、IDAT块、文件尾
文件头一般是 8950 4E47 0D0A 1A0A
而本题提示中的IHDR块是png中用来描述图片的基本信息，格式是4字节Chunk_Length、4字节Chunk_Type、13字节Chunk_Data、4字节Chunk_CRC

Chunk_Length：内容一般是13，决定了Chunk_Data的大小
Chunk_Type：内容为49484452，代表"IHDR"
Chunk_Data：4字节Width,4字节Hegiht,1字节BitDepth,1字节ColorType,1字节CompressionMethod,1字节FilterMethod,1字节InterlaceMethod
Chunk_CRC：把Chunk_Type和Chunk_Data合起来进行CRC校验


域的名称    字节数 说明
Width	4 bytes 	图像宽度，以像素为单位
Height	4 bytes 	图像高度，以像素为单位
Bit depth	1 byte	图像深度：
索引彩色图像：1，2，4或8
灰度图像：1，2，4，8或16
真彩色图像：8或16
ColorType	1 byte	颜色类型：
0：灰度图像, 1，2，4，8或16
2：真彩色图像，8或16
3：索引彩色图像，1，2，4或8
4：带α通道数据的灰度图像，8或16
6：带α通道数据的真彩色图像，8或16
Compression method 	1 byte	压缩方法(LZ77派生算法)
Filter method	1 byte	滤波器方法
Interlace method	1 byte	隔行扫描方法：
0：非隔行扫描
1： Adam7(由Adam M. Costello开发的7遍隔行扫描方法)
'''
__author__ = '__L1n__w@tch'

import requests
import binascii


def main():
    # url = "http://ctf4.shiyanbar.com/stega/IHDR.png"
    # response = requests.get(url)
    # with open("IDHR.png", "wb") as f:
    #     f.write(response.content)

    with open("IDHR.png", "rb") as f:
        data = f.read()
    chunk_type = slice(12, 16)
    chunk_data = slice(16, 29)
    print("chunk type: {}, chunk_data: {}".format(data[chunk_type], data[chunk_data]))
    ans = binascii.crc32(data[chunk_type] + data[chunk_data])
    print(hex(ans))


if __name__ == "__main__":
    main()
