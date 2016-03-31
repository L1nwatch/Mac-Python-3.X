#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 开启/关闭混杂模式: ifconfig en0 promisc/-promisc
开/关网卡: ifconfig en0 up/down
开启监听模式: ifconfig en0 mode monitor
======================================================================
将 airport 添加到路径(http://blog.csdn.net/jpiverson/article/details/22663101):
sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/sbin/airport
扫描命令：airport en0 scan。可以使用grep进行过滤，如：airport en0 scan |grep WEP或airport en0 scan |grep WPA
监听命令：sudo airport en0 sniff 6。en0是所使用网卡的名称，sniff表示模式，6表示信道。
======================================================================
其实在 sniff 给个 promisc 参数不就完事了..

'''
__author__ = '__L1n__w@tch'

from scapy.all import *

ip_list = set()


def all(packet):
    if packet.src == "ac:bc:32:7c:02:33" or packet.dst == "ac:bc:32:7c:02:33":
        return

    print("{} -> {}".format(packet.src, packet.dst))
    if packet.haslayer("ARP"):
        return
        # arp(packet)
    elif packet.haslayer("IP"):
        ip(packet, ["10.177.185.95"], "192.168.199")


def ip(packet, filter=[], prefix=""):
    if packet[IP].src in filter or packet[IP].dst in filter:
        # print(".", end="", flush=True)
        return

    # print("{} -> {}".format(packet[IP].src, packet[IP].dst))
    if packet[IP].src not in ip_list and packet[IP].src.startswith(prefix):
        print(packet.show())
        ip_list.add(packet[IP].src)
        print(ip_list)
    if packet[IP].dst not in ip_list and packet[IP].dst.startswith(prefix):
        print(packet.show())
        ip_list.add(packet[IP].dst)
        print(ip_list)

    if packet[IP].src != "192.168.43.17" and packet[IP].src != "192.168.43.43":
        pass


def arp(packet):
    print("{} -> {}".format(packet[ARP].psrc, packet[ARP].pdst))

    if packet[ARP].psrc != "192.168.43.17" and packet[ARP].psrc != "192.168.43.43":
        pass


def main():
    # pcap = ctypes.cdll.LoadLibrary(find_library("libpcap"))
    # sniff(prn=test, filter="arp", iface="en0")
    sniff(prn=all, iface="en0", promisc=0)


if __name__ == "__main__":
    main()
