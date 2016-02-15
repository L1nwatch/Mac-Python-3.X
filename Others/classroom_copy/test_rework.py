#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 对自己写的拷贝程序进行单元测试

distutils.dir_util.copy_tree没法覆盖复制的问题,参考:http://stackoverflow.com/questions/12683834/how-to-copy-directory-recursively-in-python-and-overwrite-all
解决方法是用distutils.dir_util中的copy_tree替代
'''
__author__ = '__L1n__w@tch'

import unittest
import distutils.dir_util
import os
import shutil
from try_rework import FilesSaver
import filecmp
import time

test_src = r"C:\Users\L1n\Desktop"
test_des = r"D:\goodgoodstudy"
retention = {'desktop.ini', 'Software', 'Study.lnk', '小Q屏幕截图.lnk'}
wait_time = 1


class TestSir(unittest.TestCase):
    def setUp(self):
        self.src = test_src
        self.des = test_des
        self.test_files_path = os.curdir
        self.wait_time = wait_time
        self.retention = retention

    def test_files_saver_ensure(self):
        def _test1():
            test_file_name = "just_a_file"
            test_file = os.path.join(os.curdir, "for_test", "just_a_file")
            shutil.copy(test_file, self.src)
            files_saver.ensure()
            time.sleep(self.wait_time)
            files = os.listdir(self.des)
            self.failUnless(test_file_name in files)

        def _test2():
            # TODO
            self.failUnless(True)

        def _test3():
            test_file = "just_a_file"
            shutil.copy(os.path.join("for_test", test_file), self.src)
            files_saver.ensure()

            file1 = os.path.join(self.src, test_file)
            file2 = os.path.join(self.des, test_file)

            with open(file1, "a") as f:
                f.write("test" * 30)
            time.sleep(self.wait_time)

            files_saver.ensure()

            self.failUnless(filecmp.cmp(file1, file2))

        def _test4():
            dir_name = "for_test"
            src_dir = os.path.join(self.src, "for_test")
            des_dir = os.path.join(self.des, "for_test")
            distutils.dir_util.copy_tree(dir_name, src_dir)

            files_saver.ensure()
            with open(os.path.join(src_dir, "test1"), "a") as f:
                f.write("test" * 3)
            files_saver.ensure()
            time.sleep(wait_time)
            result = filecmp.dircmp(src_dir, des_dir).diff_files
            self.failIf(len(result) <= 0)

        def _test5():
            dir_name = "for_test"
            src_dir = os.path.join(self.src, "for_test")
            des_dir = os.path.join(self.des, "for_test")
            distutils.dir_util.copy_tree(dir_name, src_dir)

            files_saver.ensure()

            result = filecmp.dircmp(src_dir, des_dir)
            self.failIf(len(result.diff_files) > 0 or len(result.left_only) > 0)

        files_saver = FilesSaver(self.src, self.des, self.retention)

        # case: 有文件复制到了源文件夹
        _test1()

        # case: 源文件夹中, retention文件列表中的文件被删除了
        _test2()

        # case: 源文件夹中, 非retention文件发生了改变
        _test3()

        # case: 源文件夹中, 非retention文件夹中的文件发生了改变
        _test4()

        # case: 有文件夹复制到了源文件夹
        _test5()

    def test_files_saver_delete(self):
        files_saver = FilesSaver(self.src, self.des, self.retention)

        test_file = os.path.join(os.curdir, "for_test", "just_a_file")
        shutil.copy(test_file, self.src)
        files_saver.delete()
        self.failIf(test_file in os.listdir(self.src))


def main():
    unittest.main()


if __name__ == "__main__":
    main()
