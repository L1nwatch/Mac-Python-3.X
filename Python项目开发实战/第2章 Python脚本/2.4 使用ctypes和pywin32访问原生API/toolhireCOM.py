#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 演示了在Python中如何使用Excel COM接口打开一个应用并让用户选择文件.
Windows Only, pywin32下载地址:http://sourceforge.net/projects/pywin32/files/pywin32/
注意要先安装好Office的Excel
'''
__author__ = '__L1n__w@tch'

import win32com.client as com


def main():
    # set the file path as required on your PC
    file_path = r"D:\PythonProject\pycharm\Python项目开发实战\第2章 Python脚本\2.4 使用ctypes和pywin32访问原生API\toolhire.xlsx"
    # 设置filemode为1,这决定会打开什么样的对话,1则打开了File-Open对话（这个值是反复试验找到的,有效值在1到4之间）
    filemode = 1  # found by trial and error!
    # Excel实际上将网格存储在另一个名为Workbook的COM对象中。如果知道哪个文件是你感兴趣的文件，就可以创建一个Workbook对
    # 象（或者更确切地说是一组Workbooks或制表符）并打开文件而不是使用一个对话框。Workbook对象包含Cells。
    # 如果想要创建或修改电子表格中的数据,则应该使用Cells
    app = com.Dispatch("Excel.Application")  # 使用Dispatch()函数创建了Application COM对象
    app.Visible = True  # 并通过设置它的Visible属性为True让窗口可见

    fd = app.FileDialog(filemode)  # 使用Application的FileDialog()方法创建了一个对话对象，它以filemode值作为参数。
    # 然后你为该对象设置了两个属性，确保它在正确的地方被打开并且拥有一个有意义的名称
    fd.InitialFileName = file_path
    fd.Title = "Open the toolhire spreadsheet"
    # 调用了对话的Show()方法将对话框显示在屏幕上。用户可以使用所有常用的功能。
    if fd.Show() == -1:  # 如果用户选择OK按钮，返回值是-1.
        fd.Execute()  # 在这种情况下，可以调用对话对象的Execute()方法来打开（或保存）被选中的文件。此时电子表格中填充的就是Workbooks的内容


if __name__ == "__main__":
    main()
