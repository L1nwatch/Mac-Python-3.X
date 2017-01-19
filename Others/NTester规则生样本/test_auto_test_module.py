#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.03 作为自动化测试模块的单元测试文件
"""
import unittest
import socket
import simplejson

__author__ = '__L1n__w@tch'

from auto_test_module import AutoTester


class TestAutoTester(unittest.TestCase):
    def setUp(self):
        self.test_json_file = "json_file_for_test.json"
        self.auto_tester = AutoTester(self.test_json_file, None, None)

    def test_get_http_headers_list(self):
        """
        测试能够从一个 json 文件中读取到对应的 http 请求, 以下截取该 json 文件中部分请求进行测试
        """
        right_answer = [
            "GET /wp-content/plugins/ajax-store-locator-wordpress/sl_file_download.php?download_file=../../passwd HTTP/1.1\r\nHost: www.nationwidemri.com\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36\r\nAccept-Encoding: gzip, deflate, sdch\r\nAccept-Language: zh-CN,zh;q=0.8,en;q=0.6\r\n\r\n",
            "POST /simple.php HTTP/1.1\r\nHost: www.shenxinfu.com\r\nConnection: keep-alive\r\nContent-Length: 54\r\nCache-Control: max-age=0\r\nOrigin: http://www.shenxinfu.com\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5\r\nContent-Type: application/x-www-form-urlencoded\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nReferer: http://www.shenxinfu.com/simple.php\r\nAccept-Encoding: gzip,deflate,sdch\r\nAccept-Language: zh-CN,zh;q=0.8\r\nAccept-Charset: GBK,utf-8;q=0.7,*;q=0.3\r\n\r\ninput=%3C%3Fphp+assert%28%24_GET%5B%27c%27%5D%29%3F%3E",
            "GET /do/vote.php?job=show&cid=%22%3E%3Ciframe%20src=http://www.zhuba.net%3E HTTP/1.1\r\nAccept: */*\r\nAccept-Language: zh-cn\r\nUser-Agent: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; LBBROWSER)\r\nAccept-Encoding: gzip, deflate\r\nHost: hnsdesyzx.hner.cn\r\nConnection: Keep-Alive\r\n\r\n",
            "GET /user_pwd/ftp/users.properties HTTP/1.1\r\nHost: 140.0.105.2\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nReferer: http://140.0.105.2/user_pwd/ftp/\r\nConnection: keep-alive\r\nPragma: no-cache\r\nCache-Control: no-cache\r\n\r\n"
        ]

        # 验证上面中的每一项都在函数执行的返回结果中
        self.assertTrue(
            all(
                [x in self.auto_tester.get_http_headers_list() for x in right_answer]
            )
        )

    def test_parse_http_header(self):
        """
        测试解析 http 头的函数是否返回正确结果
        """
        test_http = "POST /phpwind/phpwebshell/upload_file.php HTTP/1.1\r\nHost: www.shenxinfu.com\r\nConnection: keep-alive\r\nContent-Length: 339\r\nCache-Control: max-age=0\r\nOrigin: http://www.shenxinfu.com\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryXhie0pCyiDoMIDVZ\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nReferer: http://www.shenxinfu.com/phpwind/phpwebshell/up.html\r\nAccept-Encoding: gzip,deflate,sdch\r\nAccept-Language: zh-CN,zh;q=0.8\r\nAccept-Charset: GBK,utf-8;q=0.7,*;q=0.3\r\nCookie: Hm_lvt_c1a7dd239858bb744ef008b8277ae531=1341383358055\r\n\r\n"
        right_url = "/phpwind/phpwebshell/upload_file.php"
        right_header = {
            "Host": "www.shenxinfu.com",
            "Connection": "keep-alive",
            "Content-Length": "339",
            "Cache-Control": "max-age=0",
            "Origin": "http://www.shenxinfu.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryXhie0pCyiDoMIDVZ",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "http://www.shenxinfu.com/phpwind/phpwebshell/up.html",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Accept-Charset": "GBK,utf-8;q=0.7,*;q=0.3",
            "Cookie": "Hm_lvt_c1a7dd239858bb744ef008b8277ae531=1341383358055"
        }

        my_url, my_http_header = self.auto_tester.parse_http_header(test_http)
        self.assertEqual(my_url, right_url)
        self.assertEqual(my_http_header, right_header)

    def test_get_post_data_from_http_header(self):
        test_data = "POST /simple.php HTTP/1.1\r\nHost: 10.0.1.70\r\nConnection: keep-alive\r\nContent-Length: 113\r\nCache-Control: max-age=0\r\nOrigin: http://10.0.1.70\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4\r\nContent-Type: application/x-www-form-urlencoded\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nReferer: http://10.0.1.70/simple.php\r\nAccept-Encoding: gzip,deflate,sdch\r\nAccept-Language: zh-CN,zh;q=0.8\r\nAccept-Charset: GBK,utf-8;q=0.7,*;q=0.3\r\n\r\ninput=%3CSTYLE%3E%40%5C0069mport+%27http%3A%2F%2Fevil.com%2Fevil.css%27%3C%2FSTYLE%3E++&%CC%E1%BD%BB=%CC%E1%BD%BB"
        right_answer = "input=%3CSTYLE%3E%40%5C0069mport+%27http%3A%2F%2Fevil.com%2Fevil.css%27%3C%2FSTYLE%3E++&%CC%E1%BD%BB=%CC%E1%BD%BB"
        my_answer = self.auto_tester.get_post_data_from_http_header(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = "POST /jiayu/upload.php HTTP/1.1\r\nHost: 140.0.105.2\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; rv:35.0) Gecko/20100101 Firefox/35.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nReferer: http://140.0.105.2/jiayu/upload.php\r\nConnection: keep-alive\r\nContent-Type: multipart/form-data; boundary=---------------------------14597222655846\r\nContent-Length: 385\r\n\r\n-----------------------------14597222655846\r\nContent-Disposition: form-data; name=\"file\"; filename=\"test.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n<%eval\"\"&(\"e\"&\"v\"&\"a\"&\"l\"&\"(\"&\"r\"&\"e\"&\"q\"&\"u\"&\"e\"&\"s\"&\"t\"&\"(\"&\"0\"&\"-\"&\"2\"&\"-\"&\"5\"&\")\"&\")\")%>110\r\n-----------------------------14597222655846\r\nContent-Disposition: form-data; name=\"submit\"\r\n\r\nSubmit\r\n-----------------------------14597222655846--\r\n"
        right_answer = "-----------------------------14597222655846\r\nContent-Disposition: form-data; name=\"file\"; filename=\"test.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n<%eval\"\"&(\"e\"&\"v\"&\"a\"&\"l\"&\"(\"&\"r\"&\"e\"&\"q\"&\"u\"&\"e\"&\"s\"&\"t\"&\"(\"&\"0\"&\"-\"&\"2\"&\"-\"&\"5\"&\")\"&\")\")%>110\r\n-----------------------------14597222655846\r\nContent-Disposition: form-data; name=\"submit\"\r\n\r\nSubmit\r\n-----------------------------14597222655846--\r\n"
        my_answer = self.auto_tester.get_post_data_from_http_header(test_data)
        self.assertEqual(right_answer, my_answer)

        test_data = "POST /imc/webdm/mibbrowser/mibFileUpload HTTP/1.1\r\nHost: 192.200.42.215\r\nUser-Agent: Cricket-A310/1.0 UP.Browser/6.3.0.7 (GUI) MMP/2.0\r\nAccept: */*\r\nContent-Type: multipart/form-data; boundary=---------------------SXhpYSBGaWxlIFVwbG9hZA==\r\nCookie: 3C68AAAD9CD5836BEBD35AFF8DBDCEEA\r\nConnection: keep-alive\r\nContent-Length: 481\r\n"
        right_answer = ""
        my_answer = self.auto_tester.get_post_data_from_http_header(test_data)
        self.assertEqual(right_answer, my_answer)

    def test_get_sid_from_pcap_name(self):
        """
        测试获取 sid 号是否正确
        """
        test_data = "full_test/IPSv2.43_packet/web_activex/12000074_2.pcap"
        right_sid = "12000074"
        self.assertEqual(self.auto_tester.get_sid_from_pcap_name(test_data), right_sid)

        test_data = "1234.pcap"
        right_sid = "1234"
        self.assertEqual(self.auto_tester.get_sid_from_pcap_name(test_data), right_sid)

    def test_get_host_from_url(self):
        """
        测试分离 host 和 path 是否正确
        """
        test_url = "cxmdektgnpdhbers.xyz/"
        right_host, right_path = "cxmdektgnpdhbers.xyz", ""
        my_host, my_path = self.auto_tester.get_host_from_url(test_url)
        self.assertEqual(my_host, right_host)
        self.assertEqual(my_path, right_path)

        test_url = "cdn2.downloadjelly.com/9ee1efd2-b9b2-403f-8f9a-5fc856fa00a3/cancel1.gif"
        right_host, right_path = "cdn2.downloadjelly.com", "9ee1efd2-b9b2-403f-8f9a-5fc856fa00a3/cancel1.gif"
        my_host, my_path = self.auto_tester.get_host_from_url(test_url)
        self.assertEqual(my_host, right_host)
        self.assertEqual(my_path, right_path)

        test_url = "legionarios.servecounterstrike.com"
        right_host, right_path = "legionarios.servecounterstrike.com", ""
        my_host, my_path = self.auto_tester.get_host_from_url(test_url)
        self.assertEqual(my_host, right_host)
        self.assertEqual(my_path, right_path)


if __name__ == "__main__":
    with open("2th_headers_result.json", "r") as f:
        data_dict = simplejson.load(f)

    for key, value in data_dict.items():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_sock:
            my_sock.connect(("192.168.116.2", 80))
            for each_packet in value:
                print("[*] 尝试丢 {}".format(key))
                my_sock.sendall(each_packet.encode("utf8"))
    pass
