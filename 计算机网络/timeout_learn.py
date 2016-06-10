#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
''' 需要实现一个超时重传机制, 学习一下
超时装饰器链接:
http://www.cnblogs.com/fengmk2/archive/2008/08/30/python_tips_timeout_decorator.html
'''
__author__ = '__L1n__w@tch'
import time
import threading
import sys


# 网上的超时检测器
class KThread(threading.Thread):
    """A subclass of threading.Thread, with a kill()
    method.
    Come from - Kill a thread in Python:
    http://mail.python.org/pipermail/python-list/2004-May/260937.html
    """

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False

    def start(self):
        """Start the thread."""
        # 线程运行前设置跟踪过程 self.globaltrace
        self.__run_backup = self.run
        self.run = self.__run  # Force the Thread to install our trace.
        threading.Thread.start(self)  # 运行线程

    def __run(self):
        """Hacked run function, which installs the
        trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':  # 将会调用一个子过程
            return self.localtrace  # 返回调用子过程的跟踪过程self.localtrace，并使用子过程跟踪过程self.localtrace跟踪子过程运行
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':  # self._willKill自己设置的中断标识，why为跟踪的事件，其中line为执行一行或多行python代码
                raise SystemExit()  # 当中断标识为True及将会执行下一行python代码时，使用SystemExit()中断线程
        return self.localtrace

    def kill(self):
        self.killed = True


class Timeout(Exception):
    """function run timeout"""


def timeout(seconds):
    """超时装饰器，指定超时时间
    若被装饰的方法在指定的时间内未返回，则抛出Timeout异常"""

    def timeout_decorator(func):
        """真正的装饰器"""

        def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

        def _(*args, **kwargs):
            result = []
            new_kwargs = {  # create new args for _new_func, because we want to get the func return val to result list
                'oldfunc': func,
                'result': result,
                'oldfunc_args': args,
                'oldfunc_kwargs': kwargs
            }
            thd = KThread(target=_new_func, args=(), kwargs=new_kwargs)
            thd.start()
            thd.join(seconds)
            alive = thd.isAlive()
            thd.kill()  # kill the child thread
            if alive:
                raise Timeout(u'function run too long, timeout %d seconds.' % seconds)
            else:
                return result[0]

        _.__name__ = func.__name__
        _.__doc__ = func.__doc__
        return _

    return timeout_decorator


@timeout(5)
def method_timeout(seconds, text):
    print('start', seconds, text)
    time.sleep(seconds)
    print('finish', seconds, text)
    return seconds


if __name__ == '__main__':
    for sec in range(1, 10):
        try:
            print('*' * 20)
            print(method_timeout(sec, 'test waiting %d seconds' % sec))
        except Timeout as  e:
            print(e)
