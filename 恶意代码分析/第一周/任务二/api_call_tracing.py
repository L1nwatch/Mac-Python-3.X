#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 本来想在 Python3 实现 pydbg,无奈没有 py3 版本的 pydbg,自己也懒得去改, 以下复制的是网页代码,参考:
http://bbs.pediy.com/showthread.php?t=151870
'''
__author__ = '__L1n__w@tch'

'''
Author: Amit Malik
http://www.securityxploded.com
'''
"""
import sys,struct
import pefile
from pydbg import *
from pydbg.defines import *

def log(str):
  global fpp
  print str
  fpp.write(str)
  fpp.write("\n")
  return

def addr_handler(dbg):
  global func_name
  ret_addr = dbg.context.Eax
  if ret_addr:
    dict[ret_addr] = func_name
    dbg.bp_set(ret_addr,handler=generic)
  return DBG_CONTINUE

def generic(dbg):
  global func_name
  eip = dbg.context.Eip
  esp = dbg.context.Esp
  paddr = dbg.read_process_memory(esp,4)
  addr = struct.unpack("L",paddr)[0]
  addr = int(addr)
  if addr < 70000000:
    log("RETURN ADDRESS: 0x%.8x\tCALL: %s" % (addr,dict[eip]))
  if dict[eip] == "KERNEL32!GetProcAddress" or dict[eip] == "GetProcAddress":
    try:
      esp = dbg.context.Esp
      addr = esp + 0x8
      size = 50
      pstring = dbg.read_process_memory(addr,4)
      pstring = struct.unpack("L",pstring)[0]
      pstring = int(pstring)
      if pstring > 500:
        data = dbg.read_process_memory(pstring,size)
        func_name = dbg.get_ascii_string(data)
      else:
        func_name = "Ordinal entry"
      paddr = dbg.read_process_memory(esp,4)
      addr = struct.unpack("L",paddr)[0]
      addr = int(addr)
      dbg.bp_set(addr,handler=addr_handler)
    except:
      pass
  return DBG_CONTINUE


def entryhandler(dbg):
  getaddr = dbg.func_resolve("kernel32.dll","GetProcAddress")
  dict[getaddr] = "kernel32!GetProcAddress"
  dbg.bp_set(getaddr,handler=generic)
  for entry in pe.DIRECTORY_ENTRY_IMPORT:
    DllName = entry.dll
    for imp in entry.imports:
      api = imp.name
      address = dbg.func_resolve(DllName,api)
      if address:
        try:
          Dllname = DllName.split(".")[0]
          dll_func = Dllname + "!" + api
          dict[address] = dll_func
          dbg.bp_set(address,handler=generic)
        except:
          pass

  return DBG_CONTINUE

def main():
  global pe, DllName, func_name,fpp
  global dict
  dict = {}
  file = sys.argv[1]
  fpp = open("calls_log.txt",'a')
  pe = pefile.PE(file)
  dbg = pydbg()
  dbg.load(file)
  entrypoint = pe.OPTIONAL_HEADER.ImageBase + pe.OPTIONAL_HEADER.AddressOfEntryPoint
  dbg.bp_set(entrypoint,handler=entryhandler)
  dbg.run()
  fpp.close()

if __name__ == '__main__':
  main()
"""