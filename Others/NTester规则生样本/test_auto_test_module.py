#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.01.03 作为自动化测试模块的单元测试文件
"""
import unittest

__author__ = '__L1n__w@tch'

from auto_test_module import AutoTester


class TestAutoTester(unittest.TestCase):
    def setUp(self):
        self.test_json_file = "json_file_for_test.json"
        self.auto_tester = AutoTester(self.test_json_file)

    def test_get_http_headers_list(self):
        """
        测试能够从一个 json 文件中读取到对应的 http 请求, 以下截取该 json 文件中部分请求进行测试
        """
        right_answer = [
            "b'POST /phpwind/phpwebshell/upload_file.php HTTP/1.1\\r\\nHost: www.shenxinfu.com\\r\\nConnection: keep-alive\\r\\nContent-Length: 339\\r\\nCache-Control: max-age=0\\r\\nOrigin: http://www.shenxinfu.com\\r\\nUser-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11\\r\\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryXhie0pCyiDoMIDVZ\\r\\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\\r\\nReferer: http://www.shenxinfu.com/phpwind/phpwebshell/up.html\\r\\nAccept-Encoding: gzip,deflate,sdch\\r\\nAccept-Language: zh-CN,zh;q=0.8\\r\\nAccept-Charset: GBK,utf-8;q=0.7,*;q=0.3\\r\\nCookie: Hm_lvt_c1a7dd239858bb744ef008b8277ae531=1341383358055\\r\\n\\r\\n'",
            "b'POST /phpwind/phpwebshell/upload_file.php HTTP/1.1\\r\\nHost: www.shenxinfu.com\\r\\nConnection: keep-alive\\r\\nContent-Length: 339\\r\\nCache-Control: max-age=0\\r\\nOrigin: http://www.shenxinfu.com\\r\\nUser-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11\\r\\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryXhie0pCyiDoMIDVZ\\r\\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\\r\\nReferer: http://www.shenxinfu.com/phpwind/phpwebshell/up.html\\r\\nAccept-Encoding: gzip,deflate,sdch\\r\\nAccept-Language: zh-CN,zh;q=0.8\\r\\nAccept-Charset: GBK,utf-8;q=0.7,*;q=0.3\\r\\nCookie: Hm_lvt_c1a7dd239858bb744ef008b8277ae531=1341383358055\\r\\n\\r\\n------WebKitFormBoundaryXhie0pCyiDoMIDVZ\\r\\nContent-Disposition: form-data; name=\"file\"; filename=\"script.php\"\\r\\nContent-Type: application/php\\r\\n\\r\\n<script language=\"php\">@eval_r($_POST[sb])</script>\\r\\n------WebKitFormBoundaryXhie0pCyiDoMIDVZ\\r\\nContent-Disposition: form-data; name=\"submit\"\\r\\n\\r\\nsubmit\\r\\n------WebKitFormBoundaryXhie0pCyiDoMIDVZ--\\r\\n'",
            "b'GET /dvwa/abc.php?id=os.rename(%22a%22); HTTP/1.1\\r\\nHost: 10.0.1.151\\r\\nConnection: keep-alive\\r\\nCache-Control: max-age=0\\r\\nUser-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1\\r\\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\\r\\nAccept-Encoding: gzip,deflate,sdch\\r\\nAccept-Language: zh-CN,zh;q=0.8\\r\\nAccept-Charset: GBK,utf-8;q=0.7,*;q=0.3\\r\\nCookie: security=low; PHPSESSID=2f180973cde8043c5051efcf57181bae\\r\\n\\r\\n'",
            "b'GET /dvwa/abc.php?id=os.rename(%22a%22); HTTP/1.1\\r\\nHost: 10.0.1.151\\r\\nConnection: keep-alive\\r\\nCache-Control: max-age=0\\r\\nUser-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1\\r\\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\\r\\nAccept-Encoding: gzip,deflate,sdch\\r\\nAccept-Language: zh-CN,zh;q=0.8\\r\\nAccept-Charset: GBK,utf-8;q=0.7,*;q=0.3\\r\\nCookie: security=low; PHPSESSID=2f180973cde8043c5051efcf57181bae\\r\\n\\r\\n'"]

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
        test_http = "b'POST /phpwind/phpwebshell/upload_file.php HTTP/1.1\\r\\nHost: www.shenxinfu.com\\r\\nConnection: keep-alive\\r\\nContent-Length: 339\\r\\nCache-Control: max-age=0\\r\\nOrigin: http://www.shenxinfu.com\\r\\nUser-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11\\r\\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryXhie0pCyiDoMIDVZ\\r\\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\\r\\nReferer: http://www.shenxinfu.com/phpwind/phpwebshell/up.html\\r\\nAccept-Encoding: gzip,deflate,sdch\\r\\nAccept-Language: zh-CN,zh;q=0.8\\r\\nAccept-Charset: GBK,utf-8;q=0.7,*;q=0.3\\r\\nCookie: Hm_lvt_c1a7dd239858bb744ef008b8277ae531=1341383358055\\r\\n\\r\\n'"
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
            "Cookie": "Hm_lvt_c1a7dd239858bb744ef008b8277ae531=134138335805"
        }

        my_url, my_http_header = self.auto_tester.parse_http_header(test_http)
        self.assertEqual(my_url, right_url)
        self.assertEqual(my_http_header, right_header)


if __name__ == "__main__":
    pass
