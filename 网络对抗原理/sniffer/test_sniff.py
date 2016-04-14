#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 测试 sniff 用的
'''
__author__ = '__L1n__w@tch'

from scapy.all import *
import io
from contextlib import redirect_stdout
from collections import OrderedDict
import threading

semaphore = threading.Semaphore(0)


class SniffThread(threading.Thread):
    def __init__(self):
        super(SniffThread, self).__init__()
        global semaphore

        self.stopped = False

    def prn(self, packet):
        global semaphore

        with io.StringIO() as buf, redirect_stdout(buf):
            packet.show()
            output = buf.getvalue()
        if "TCP" in output:
            print(output)
        elif "UDP" in output:
            print(output)
        else:
            print(output[:3], end="")

        if self.stopped:
            p(semaphore)

    def run(self):
        sub_thread = threading.Thread(
            target=lambda: sniff(prn=self.prn, iface="en0", promisc=1, store=0,
                                 lfilter=lambda x: x.haslayer("TCP")))
        sub_thread.start()

    def stop(self):
        self.stopped = True

    def restart(self):
        self.stopped = False
        v(semaphore)


def v(semaphore):
    semaphore.release()


def p(semaphore):
    semaphore.acquire()


def lfilter_func(packet):
    d_configuration = OrderedDict()
    d_configuration["TCP"] = False
    d_configuration["UDP"] = False
    d_configuration["ICMP"] = True
    d_configuration["ARP"] = False
    d_configuration["Others"] = True

    for protocol in d_configuration:
        if protocol != "Others":
            if packet.haslayer(protocol) and not d_configuration[protocol]:
                return False
        elif d_configuration["Others"]:
            return True
    return True


if __name__ == "__main__":
    res = sniff(prn=lambda x: x.summary(), iface="en0", promisc=1, lfilter=lfilter_func)
    print(res)
    # sniff_thread = SniffThread()
    # sniff_thread.start()

    # input("Stop?")
    # sniff_thread.stop()
    # input("Restart?")
    # sniff_thread.restart()
