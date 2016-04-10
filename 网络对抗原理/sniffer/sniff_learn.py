#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

from scapy.all import *
import sys
from io import StringIO

# import logging
# logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # 清除报错

# 配置各种信息，以便调用
localmac = 'ac:bc:32:7c:02:33'
localip = '192.168.43.43'
destip = '192.168.43.1'
ifname = 'en0'


def dns_acquire():
    dns_name = "www.baidu.com"

    f_handler = StringIO()
    __console__ = sys.stdout
    sys.stdout = f_handler

    ip_frame = IP(dst="114.114.114.114")
    udp_frame = UDP()
    dns_frame = DNS(rd=1, qd=DNSQR(qname=dns_name))
    packet = ip_frame / udp_frame / dns_frame
    dns_result = sr(packet, verbose=False)
    # print(dns_result)

    # [!]
    dns_result[0][0][1].show()
    sys.stdout = __console__
    dns_raw = f_handler.getvalue()

    result_type = re.findall('.*\s+(type)\s*=\s*(.*).*', dns_raw)
    result_data = re.findall('.*\s+(rdata)\s*=\s*(.*).*', dns_raw)
    result_type_data = zip(result_type, result_data)
    for x, y in result_type_data:
        print('%s %-5s %s %s' % (x[0], x[1], y[0], y[1]))


def arp_sr():
    """
    广播一个 arp 请求, 获取 destip 对应的 MAC 地址
    :return:
    """
    ether_frame = Ether(src=localmac, dst='FF:FF:FF:FF:FF:FF')
    arp_frame = ARP(op=1, hwsrc=localmac, hwdst='00:00:00:00:00:00', psrc=localip, pdst=destip)
    packet = ether_frame / arp_frame

    # [!] verbose is True [*]
    #     Begin emission:
    # Finished to send 1 packets.
    #
    # Received 2 packets, got 1 answers, remaining 0 packets
    '''
    sr() function is for sending packets and receiving answers. The function #returns a couple of packet and answers, and the unanswered packets.
    sr1() is a variant that only return one packet that answered the packet (or #the packet set) sent. The packets must be layer 3 packets (IP, ARP, etc.).
    srp() do the same for layer 2 packets (Ethernet, 802.3, etc.).
    '''
    result_raw = srp(packet, iface=ifname, verbose=False)
    # result_raw == <Results: TCP:0 UDP:0 ICMP:0 Other:1>, <Unanswered: TCP:0 UDP:0 ICMP:0 Other:0>
    # type(result_raw[0]) == <class 'scapy.plist.SndRcvList'>
    result_list = result_raw[0].res  # res: the list of packets
    # 一个列表，每一个item为一个元组，元组内包括一次ARP请求与回应
    # result_list == [(<Ether  dst=.. src=.. type=.. |<ARP  op=.. hwsrc=.. psrc=.. hwdst=.. pdst=.. |>>, <Ether  dst=.. src=.. type=.. |<ARP  hwtype=.. ptype=.. hwlen=.. plen=.. op=.. hwsrc=.. psrc=.. hwdst=.. pdst=.. |<Padding load=‘..’ |>>>)]
    ether_frame = result_list[0][1][0]
    arp_frame = result_list[0][1][1]
    print(ether_frame.fields)
    # 以太网头部字段: {'dst': 'FF:FF:FF:FF:FF:FF', 'src': 'ac:bc:32:7c:02:33'}
    print(arp_frame.fields)
    # ARP头部字段: {'src': 'b4:0b:44:2d:d4:ee', 'dst': 'ac:bc:32:7c:02:33', 'type': 2054}
    print("IP地址: {}, MAC 地址: {}".format(result_list[0][1][1].fields['psrc'], result_list[0][1][1].fields['hwsrc']))


if __name__ == "__main__":
    # arp_sr()
    dns_acquire()
