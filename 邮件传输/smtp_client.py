#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 尝试实现邮件客户端

2017.04.23 参考菜鸟教程进行尝试, 发送邮件到 qq 邮箱中, 后来发现别人把这个都标识为垃圾邮件了= =
"""
import smtplib
from email.mime.text import MIMEText
from email.header import Header

__author__ = '__L1n__w@tch'


class MySMTPClient:
    def __init__(self):
        self.user_name = "xxxxx@163.com"
        self.password = "xxxxx"

    def run(self):
        smtp_server = "smtp.163.com"
        sender = 'xxxxx@163.com'  # 要求 sender 必须和认证过的邮箱保持一致
        receivers = ["yyyyy@wo.cn"]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
        mail_content = '尝试实现邮件客户端 2017.04.23 参考菜鸟教程进行尝试, 发送邮件到 qq 邮箱中'.format(receivers)

        message = MIMEText(mail_content, 'plain', 'utf-8')
        message['From'] = Header("xxxx<{}>".format(self.user_name), 'utf-8')  # 发件人名称
        message['To'] = Header(";".join(receivers), 'utf-8')  # 收件人名称

        subject = '为啥老是发送失败?'  # 邮件标题
        message['Subject'] = Header(subject, 'utf-8')

        try:
            server = smtplib.SMTP(smtp_server)
            server.set_debuglevel(1)  # 用 set_debuglevel(1) 就可以打印出和 SMTP 服务器交互的所有信息
            server.starttls()  # 加密 SMTP, QQ 邮箱要求的
            server.login(self.user_name, self.password)  # 账号密码登录
            server.sendmail(sender, receivers, message.as_string())  # 确保本机有 send_mail 程序
        except smtplib.SMTPServerDisconnected as e:
            print("[-] 服务器拒绝登录, 消息为: {}".format(e))
        finally:
            server.close()


if __name__ == "__main__":
    MySMTPClient().run()
