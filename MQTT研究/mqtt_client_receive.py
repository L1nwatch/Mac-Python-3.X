#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("chat")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.username_pw_set("test", "test")  # 必须设置，否则会返回「Connected with result code 4」
client.on_connect = on_connect
client.on_message = on_message


print("[*] 开始尝试连接")
client.connect("192.168.1.59", 1883)
client.publish("chat","hello watch login",2)
print("[*] 连接完毕，开始循环监听")
client.loop_forever()

__author__ = '__L1n__w@tch'

if __name__ == "__main__":
    pass
