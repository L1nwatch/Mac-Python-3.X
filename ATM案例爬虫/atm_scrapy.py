#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.07.22 修正 atm 下载工具会新增多余换行符的问题
2016.12.02 修正文件夹如果存在空格会导致 Windows 下运行出错的问题, 另外添加跳过文件夹功能
2016.11.27 爬虫正常了, 加入参数使用吧, 打包发现 queue 报错, 需要手动导入, 另外路径参数有点问题, 已修正
2016.11.26 陆续编写, 到今天终于可以完成下载功能了, 简称爬虫 v1.0
2016.11.20 发现 ATM 本身就提供导出案例的功能, 不过是导出成 excel 格式的
2016.11.16 爬虫, 爬取公司上的 ATM 平台的案例, 要不然学习别人的案例学习起来不方便
"""
import queue
import chardet
import argparse
import requests
import os
import re
import datetime
import pymysql
from my_constant import const

try:
    import simplejson as json
except ImportError:
    import json

__author__ = '__L1n__w@tch'


class ATMScrapy:
    def __init__(self, project_url, path_dir=os.curdir, sql_connector=None, cases_filter=None):
        self.project_id = self.get_project_id_from_url(project_url)
        self.mysql = sql_connector
        self.case_table_name = "t_atm_cases"
        self.cases_filter = cases_filter

        # 初始化默认下载目录
        if path_dir == os.curdir:
            today = datetime.datetime.now()
            self.path_dir = os.path.join(path_dir, "ATM爬虫-{year}{month}{day}-{hour}{minute}".format(
                year=today.year, month=today.month, day=today.day,
                hour=str(today.hour).zfill(2), minute=str(today.minute).zfill(2)))
        else:
            self.path_dir = path_dir

        os.makedirs(self.path_dir, exist_ok=True)

    def crawl(self):
        """
        执行整体爬虫流程
        :return:
        """
        # 数据库判断
        if self.mysql is not None:
            self.mysql.create_tables_for_case(self.case_table_name)
            print("[!] 创建表 {} 成功, 接下来会将案例写进数据库而不是保存到文件中".format(self.case_table_name))

        # 下载并解析 json 文件
        json_file_path = self.download_tree_json_file()
        parse_result = self.parse_tree_json_file(json_file_path)

        # 创建对应文件夹/文件, 并保存 id 号
        result = self.create_case_trees_from_list(parse_result)

        os.remove(json_file_path)

        return result

    def download_tree_json_file(self, project_id=None):
        """
        下载整体的 json 文件
        :param project_id: 项目的 id
        :return:
        """
        if project_id is None:
            project_id = self.project_id
        response = requests.get(url="http://200.200.0.33/atm/projects/{}/suites".format(project_id))

        json_file_path = "{}.json".format(self.project_id)
        with open(json_file_path, "w") as f:
            f.write(response.text)

        return json_file_path

    @staticmethod
    def get_project_id_from_url(project_url):
        """
        从给定的 url 中解析出项目 id
        :param project_url: "http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec"
        :return: "53c49025d105401f5e0003ec"
        """
        try:
            project_id = re.findall(".*([0-9a-zA-Z]{24}).*", project_url)[0]
        except IndexError:
            raise IndexError("[!] URL 是不是有问题啊你")
        all_possible_id = re.findall("([0-9a-zA-Z]*)", project_url)

        if all(possible_id != project_id for possible_id in all_possible_id):
            raise RuntimeError
        return project_id

    @staticmethod
    def parse_tree_json_file(file_path):
        """
        负责解析 json 文件并且创建对应文件夹及文件
        :param file_path:
        :return:
        """
        with open(file_path, "r") as f:
            result = json.load(f)

        return result

    def create_case_trees_from_list(self, a_list, path_dir=None):
        """
        根据一个列表创建对应的文件夹, 文件
        :param a_list: json 格式的一个列表
        :param path_dir: 下载文件夹的根目录
        :return:
        """
        if path_dir is None:
            path_dir = self.path_dir

        def __recursion_create_dirs(children_list, root_path):
            for each_kid in children_list:
                if self.cases_filter and each_kid["name"] in self.cases_filter:
                    print("[!] 用户选择跳过 {} 文件夹的下载...".format(each_kid["name"]))
                    continue

                cases_dir_name = self.get_safe_name(each_kid["name"])
                dir_path = os.path.join(root_path, cases_dir_name)
                os.makedirs(dir_path, exist_ok=True)

                print("[!] 下载 {} 中...".format(cases_dir_name))

                # 不是最后一级目录
                if len(each_kid["children"]) > 0:
                    __recursion_create_dirs(each_kid["children"], dir_path)
                # 已经是最后一级目录了
                else:
                    self.create_cases_from_cases_id(each_kid["id"], dir_path)

        __recursion_create_dirs(a_list, path_dir)

        return const.SUCCESS_MESSAGE

    @staticmethod
    def get_safe_name(raw_name):
        """
        过滤掉特殊字符
        :param raw_name: 原来的名字, 可能包含特殊字符
        :return: 不包含特殊字符的名字
        """
        special_char = ["\\", "/", "*", ":", "?", '"', ">", "<", "|"]
        result = raw_name
        for each_char in special_char:
            result = result.replace(each_char, "-")
        return result.strip()

    def create_cases_from_cases_id(self, cases_id, cases_path):
        """
        根据字典, 在不同文件夹下创建对应的案例
        :param cases_id: cases 的 id, 通过这个 id 可以获取到这个文件夹下的所有案例
        :param cases_path: 要放置的目录
        :return:
        """
        cases_url = "http://200.200.0.33/atm/projects/{}/suites?id={}".format(self.project_id, cases_id)

        # 获取最后一级目录中所有案例 id, 保存到 json 中
        response = requests.get(cases_url)
        json_file_path = "{}.json".format(cases_id)
        with open(json_file_path, "w") as f:
            f.write(response.text)

        # 解析保存的 json 文件, 创建对应案例
        a_list = self.parse_tree_json_file(json_file_path)
        for each_case in a_list:
            if self.mysql is None:
                self.write_case_into_file(each_case, cases_path)
            else:
                self.write_case_into_db(each_case, cases_path)

        os.remove(json_file_path)

    def write_case_into_db(self, case, cases_path):
        """
        将下载到的案例写入数据库中
        :param case: 案例
        :param cases_path: 案例所在的根目录
        :return:
        """
        try:
            case_id = case["id"]
            case_name = self.get_safe_name(case["name"])
            case_path = os.path.join(cases_path, case_name)
            case_content = self.get_case_content_from_case_id(case_id)
        except Exception as e:
            print("[!] 下载文件: {} 中的 {} 出错".format(cases_path, case))
            raise e

        self.mysql.insert_data_to_case_table(self.case_table_name, case_id, case_path, case_content)

    def write_case_into_file(self, case, cases_path):
        """
        将下载到的案例写入文件中
        :param case: 案例字典, 包括名称, id 等
        :param cases_path: 案例所在的根目录
        :return:
        """
        name = "{}.txt".format(self.get_safe_name(case["name"]))
        case_file_path = os.path.join(cases_path, name)
        case_content = self.get_case_content_from_case_id(case["id"])

        try:
            # 统一换行符
            case_content = case_content.replace("\r\n", "\n")

            with open(case_file_path, "w") as f:
                f.write(case_content)
        except UnicodeEncodeError as e:
            print("[!] 文件 {} 存在编码问题, 转成 utf8 编码".format(case_file_path))
            with open(case_file_path, "w", encoding="utf8") as f:
                f.write(case_content)

    def get_case_content_from_case_id(self, case_id):
        """
        给定一个 id, 获取其内容后返回
        :param case_id: "5832d192d105400a3100006e"
        :return: 案例的内容, str 形式
        """
        case_content_url = "http://200.200.0.33/atm/projects/{}/usecases/{}".format(self.project_id, case_id)
        response = requests.get(case_content_url)

        return response.text

    @staticmethod
    def get_right_encoding_content(raw_content):
        """
        涉及编码问题,尝试解决
        :param raw_content: 二进制数据, 待解码
        :return: 文件内容, str() 形式
        """
        encoding = chardet.detect(raw_content)["encoding"]

        try:
            data = raw_content.decode("utf8")
        except UnicodeDecodeError:
            try:
                data = raw_content.decode("gbk")
            except UnicodeDecodeError:
                data = raw_content.decode(encoding)

        return data


class DBConnector:
    def __init__(self, host, user, passwd, db="", charset="utf8"):
        self.db_connector = pymysql.connect(host=host, user=user, passwd=passwd, db=db, charset=charset)
        self.db_cursor = self.db_connector.cursor()

    def create_tables_for_case(self, table_name):
        """
        为案例创建表格, 字段是固定死的
        :param table_name: 表格名
        :return:
        """
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        self.db_cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))

        # 使用预处理语句创建表
        sql = ("""CREATE TABLE {} (
               case_id CHAR(24) NOT NULL,
               case_path TEXT NOT NULL,
               case_content TEXT,
               PRIMARY KEY (case_id) )""".format(table_name)
               )

        self.db_cursor.execute(sql)

    def insert_data_to_case_table(self, table_name, case_id, case_path, case_content):
        """
        插入数据到案例表格中对应字段
        :param table_name: 表格名字, 比如 "t_atm_cases"
        :param case_id: 固定 24 个字符, 比如 "57eb3d9ed10540526e001170"
        :param case_path: 案例的路径, 比如 "预发布测试项/前置/大家好"
        :param case_content: 案例的内容, 比如 "[我只是个虚拟的关键字]"
        :return:
        """
        safe_case_content = pymysql.escape_string(case_content)

        # SQL 插入语句
        sql = r"INSERT INTO {}(case_id, case_path, case_content) VALUES ('{}', '{}', '{}')" \
            .format(table_name, case_id, case_path, safe_case_content)

        # print("[!!] 尝试写入数据: {}".format(safe_case_content))

        try:
            # 执行sql语句
            self.db_cursor.execute(sql)
            # 提交到数据库执行
            self.db_connector.commit()
        except Exception as e:
            # 如果发生错误则回滚
            self.db_connector.rollback()
            raise e

    def query_data_from_case_table(self, table_name, limit_number=100):
        """
        从案例表格中读取数据
        :param table_name: 表格名字, 比如 "t_atm_cases"
        :param limit_number: 限制读取多少条, 比如 100
        :return:
        """
        # SQL 查询语句
        sql = "SELECT * FROM {} LIMIT {}".format(table_name, limit_number)
        try:
            # 执行SQL语句
            self.db_cursor.execute(sql)
            # 获取所有记录列表
            results = self.db_cursor.fetchall()
            print(results)
        except Exception as e:
            print("[!] 获取数据失败")
            raise e

    def close_db(self):
        """
        关闭数据库连接
        :return:
        """
        self.db_connector.close()


def add_argument(parser):
    """
    为解析器添加参数
    :param parser: ArgumentParser 实例对象
    :return: None
    """
    parser.add_argument("--path", "-p", type=str,
                        default=os.curdir, help="指定存放路径")
    parser.add_argument("--url", "-u", type=str, required=True, help="项目的链接, 也可以直接输入项目 id")
    parser.add_argument("--db", "-d", type=str, required=False,
                        help="选择写入数据库中, 格式比如:'localhost#root#password#TESTDB#utf8', 分别表示'主机#用户名#密码#数据库名#编码'")
    parser.add_argument("--skip", "-s", type=str, required=False, help="想跳过的文件夹, 格式比如 '回收站#AF7.0'")


def set_argument(options):
    """
    读取用户输入的参数, 检验是否合法
    :param options: parser.opts
    :return: dict()
    """
    configuration = dict()
    configuration["path"] = options.path
    configuration["url"] = options.url
    configuration['db'] = options.db
    configuration['skip'] = options.skip

    print("[*] 指定存放的路径为: {}".format(configuration["path"]))
    print("[*] 指定项目 url 为: {}".format(configuration["url"]))
    print("[*] 指定数据库信息为: {}".format(configuration["db"])) if configuration["db"] else None
    print("[*] 用户指定不爬取文件夹: {}".format(configuration["skip"])) if configuration["skip"] else None

    return configuration


def initialize():
    """
    进行初始化操作, 包括 arg_parse 解析程序的初始化, 参数的相关设定等
    :return: path, file_type, keyword
    """
    parser = argparse.ArgumentParser(description="ATM 案例爬虫 v2.0-Author: 林丰35516")
    add_argument(parser)
    configuration = set_argument(parser.parse_args())

    db_connector = None
    if configuration["db"] is not None:
        host, user, password, db_name, charset = configuration["db"].split("#")
        db_connector = DBConnector(host, user, password, db_name, charset)

    skip_dirs_list = None
    if configuration["skip"] is not None:
        skip_dirs_list = configuration["skip"].split("#")

    return configuration["url"], configuration["path"], db_connector, skip_dirs_list


if __name__ == "__main__":
    # atm_project_url = "http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec/suites"
    # case_url = "http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec/suites?id=57eb3d9ed10540526e00116f"
    # case_content = "http://200.200.0.33/atm/projects/53c49025d105401f5e0003ec/usecases/5832d192d105400a3100006e"

    print("[*] ATM 案例爬虫 v2.0-Author: 林丰35516")
    url, path, db, skip_dirs = initialize()
    project_id = ATMScrapy.get_project_id_from_url(url)

    print("[*] {sep} 开始爬项目{project_id} {sep}".format(sep="=" * 30, project_id=project_id))

    my_atm_crawl = ATMScrapy(project_id, path, db, skip_dirs)
    my_atm_crawl.crawl()

    print("[*] {sep} 项目{project_id}爬取完毕 {sep}".format(sep="=" * 30, project_id=project_id))
    input("[?] 输入任意键退出")
