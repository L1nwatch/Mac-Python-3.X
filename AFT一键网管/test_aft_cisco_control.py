#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
作为单元测试文件存在
"""
import unittest
from aft_cisco_control import AFTCiscoControl

__author__ = '__L1n__w@tch'


class TestAFTCiscoControl(unittest.TestCase):
    def setUp(self):
        self.aft_c_c = AFTCiscoControl(None)

    def test_extract_inout_information(self):
        """
        测试提取进出口流量是否正确
        """
        test_data = b'show  interfaces fastEthernet 0/1\r\nFastEthernet0/1 is up, line protocol is up (connected)\r\n  Hardware is Fast Ethernet, address is 8cb6.4ff0.9481 (bia 8cb6.4ff0.9481)\r\n  MTU 1500 bytes, BW 100000 Kbit, DLY 100 usec, \r\n     reliability 255/255, txload 1/255, rxload 1/255\r\n  Encapsulation ARPA, loopback not set\r\n  Keepalive set (10 sec)\r\n  Full-duplex, 100Mb/s, media type is 10/100BaseTX\r\n  input flow-control is off, output flow-control is unsupported \r\n  ARP type: ARPA, ARP Timeout 04:00:00\r\n  Last input 1w2d, output 00:00:01, output hang never\r\n  Last clearing of "show interface" counters never\r\n  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0\r\n  Queueing strategy: fifo\r\n  Output queue: 0/40 (size/max)\r\n  5 minute input rate 16000 bits/sec, 18 packets/sec\r\n  5 minute output rate 194000 bits/sec, 325 packets/sec\r\n     627443870 packets input, 91227676106 bytes, 0 no buffer\r\n     Received 303573382 broadcasts (0 multicasts)\r\n     0 runts, 0 giants, 0 throttles\r\n     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored\r\n     0 watchdog, 40936745 multicast, 0 pause input\r\n     0 input packets with dribble condition detected\r\n     621614154 packets output, 201910001121 bytes, 0 underruns\r\n --More-- \x08\x08\x08\x08\x08\x08\x08\x08\x08        \x08\x08\x08\x08\x08\x08\x08\x08\x08     0 output errors, 0 collisions, 1 interface resets\r\n     0 babbles, 0 late collision, 0 deferred\r\n     0 lost carrier, 0 no carrier, 0 PAUSE output\r\n     0 output buffer failures, 0 output buffers swapped out\r\nAF#'
        # right_answer = b"5 minute input rate 16000 bits/sec, 18 packets/sec\r\n  5 minute output rate 194000 bits/sec, 325 packets/sec\r\n"
        # 需求变更，提取出两个数字即可
        right_answer = (b"18", b"325")
        my_answer = self.aft_c_c.extract_inout_information(test_data)
        self.assertEqual(right_answer, my_answer)
