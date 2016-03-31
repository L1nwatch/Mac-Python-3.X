#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' Description
'''
__author__ = '__L1n__w@tch'

# !/usr/bin/env python3.2

import ctypes, sys
from ctypes.util import find_library

# required so we can access bpf_program->bf_insns
"""
struct bpf_program {
    u_int bf_len;
    struct bpf_insn *bf_insns;}
"""


class bpf_program(ctypes.Structure):
    _fields_ = [("bf_len", ctypes.c_int), ("bf_insns", ctypes.c_void_p)]


class sockaddr(ctypes.Structure):
    _fields_ = [("sa_family", ctypes.c_uint16), ("sa_data", ctypes.c_char * 14)]


class pcap_pkthdr(ctypes.Structure):
    _fields_ = [("tv_sec", ctypes.c_long), ("tv_usec", ctypes.c_long), ("caplen", ctypes.c_uint),
                ("len", ctypes.c_uint)]


def main():
    # pcap = ctypes.cdll.LoadLibrary("libpcap.so")
    pcap = ctypes.cdll.LoadLibrary(find_library("libpcap"))

    pcap_lookupdev = pcap.pcap_lookupdev
    pcap_lookupdev.restype = ctypes.c_char_p
    # pcap_lookupnet(dev, &net, &mask, errbuf)
    pcap_lookupnet = pcap.pcap_lookupnet
    # pcap_t *pcap_open_live(const char *device, int snaplen,int promisc, int to_ms, char *errbuf)
    pcap_open_live = pcap.pcap_open_live
    pcap_open_live.restype = ctypes.c_char_p
    # int pcap_compile(pcap_t *p, struct bpf_program *fp,const char *str, int optimize, bpf_u_int32 netmask)
    pcap_compile = pcap.pcap_compile
    # int pcap_setfilter(pcap_t *p, struct bpf_program *fp)
    pcap_setfilter = pcap.pcap_setfilter
    # const u_char *pcap_next(pcap_t *p, struct pcap_pkthdr *h)
    pcap_next = pcap.pcap_next

    # prepare args
    snaplen = ctypes.c_int(1540)
    linktype = ctypes.c_int(12)  # DLT_RAW on linux
    program = bpf_program()
    # buf = ctypes.c_char_p(filter)
    optimize = ctypes.c_int(0)
    mask = ctypes.c_int(0)

    errbuf = ctypes.create_string_buffer(256)

    dev = pcap_lookupdev(errbuf)
    dev = bytes(str('en0'), 'ascii')

    if (dev):
        print("{0} is the default interface".format(dev))
    else:
        print("Was not able to find default interface {0}".format(errbuf.value))

    mask = ctypes.c_uint(32)
    net = ctypes.c_uint(32)

    if (pcap_lookupnet(dev, ctypes.pointer(net), ctypes.pointer(mask), errbuf) == -1):
        print("Error could not get netmask for device {0}".format(errbuf.value))
        sys.exit(0)
    else:
        print("Got Required netmask")

    to_ms = ctypes.c_int(1000)
    promisc = ctypes.c_int(1)
    handle = pcap_open_live(dev, snaplen, promisc, to_ms, errbuf)

    if (handle is False):
        print("Error unable to open session : {0}".format(errbuf.value))
        sys.exit(0)
    else:
        print("Pcap open live worked!")

    filter = bytes(str('port 80'), 'ascii')
    buf = ctypes.c_char_p(filter)

    if (pcap_compile(handle, ctypes.byref(program), buf, ctypes.c_int(1), mask) == -1):
        # this requires we call pcap_geterr() to get the error
        print("Error could not compile bpf filter because {0}".format(errbuf.value))
    else:
        print("Filter Compiled!")

    if (pcap_setfilter(handle, ctypes.byref(program) == -1)):
        print("Error couldn't install filter {0}".format(errbuf.value))
        sys.exit(0)
    else:
        print("Filter installed!")

    header = pcap_pkthdr()
    if (pcap_next(handle, ctypes.bref(header)) == -1):
        print("ERROR pcap_next failed!")

    print("Got {0} bytes of data".format(pcap_pkthdr().len))
    pcap_close = pcap.pcap_close
    pcap_close(handle)


if __name__ == "__main__":
    main()
