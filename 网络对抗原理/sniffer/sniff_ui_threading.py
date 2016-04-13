#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
'''
多进程版本,发现不太好共享变量,所以还是全部改写成多线程好了

用于实现嗅探器的 UI 界面, 本来想用 PyQt 写的, 但是还没学, 而且时间不够, 所以还是用 tkinter 实现了

突然发现 LabelFrame 比 Frame 好看些, 至少在 Mac 下是的(至少在我的审美观下是的)
'''
__author__ = '__L1n__w@tch'

import tkinter
import sys
import threading
import io
import tkinter.messagebox as mb
from contextlib import redirect_stdout
from collections import OrderedDict
from my_sniffer import MySniffer, l_packets
from scapy.utils import sane_color, orb


class MyUI:
    def __init__(self):
        global l_packets
        self.d_packets_counts = {"TCP": 0, "UDP": 0, "ICMP": 0, "ARP": 0, "Others": 0}

        # 嗅探线程
        self.my_sniffer = MySniffer()
        sniff_thread = threading.Thread(target=self.my_sniffer.sniff, args=list())
        sniff_thread.start()

        ### 主窗口
        self.root = tkinter.Tk()
        self._initialize_root(self.root)

        ## 菜单栏
        menu_frame = tkinter.Frame(self.root)
        self._initialize_menu(menu_frame)

        ## 功能实现区 Start
        # 列表帧, 包括包数量列表, 包列表区域 #TODO: 本来第一个是 IP 列表区域的,待定
        packets_frame = tkinter.LabelFrame(self.root)
        self._initialize_list_frame(packets_frame)

        # 内容显示帧, 包括图形化显示/其余功能选项区域, 内容显示区域
        content_frame = tkinter.LabelFrame(self.root)
        self._initialize_content_frame(content_frame)
        ## 功能实现区 End

        ## 状态栏
        # state_frame = tkinter.Frame(self.root)

        self.root.mainloop()

    def _counts_packets_type(self, packet):
        if packet.haslayer("TCP"):
            self.d_packets_counts["TCP"] += 1
        elif packet.haslayer("UDP"):
            self.d_packets_counts["UDP"] += 1
        elif packet.haslayer("ICMP"):
            self.d_packets_counts["ICMP"] += 1
        elif packet.haslayer("ARP"):
            self.d_packets_counts["ARP"] += 1
        else:
            self.d_packets_counts["Others"] += 1

    def _update_packets_list(self, listbox):
        global l_packets

        # 保存包列表到类变量中
        self.l_packets = list()

        while True:
            # 检查是否有抓到新的包
            if len(l_packets) > len(self.l_packets):
                ## 更新包列表 Start
                # 有新的包, 保存进类变量里, 并且打印到图形界面的包列表区域中
                for index in range(len(self.l_packets), len(l_packets)):
                    print_data = "{:<10}{:<}".format(index, l_packets[index].summary())
                    self.l_packets.append(l_packets[index])
                    listbox.insert(tkinter.END, print_data)
                    # listbox.yview(tkinter.END)  # 自动滚动到最下面
                    ## 更新包列表 End

                    ## 更新包数量列表 Start
                    self._counts_packets_type(l_packets[index])
                    self.packets_num_listbox.delete(0, tkinter.END)
                    self.packets_num_listbox.insert(tkinter.END, "TCP:{}".format(self.d_packets_counts["TCP"]))
                    self.packets_num_listbox.insert(tkinter.END, "UDP:{}".format(self.d_packets_counts["UDP"]))
                    self.packets_num_listbox.insert(tkinter.END, "ICMP:{}".format(self.d_packets_counts["ICMP"]))
                    self.packets_num_listbox.insert(tkinter.END, "ARP:{}".format(self.d_packets_counts["ARP"]))
                    self.packets_num_listbox.insert(tkinter.END, "Others:{}".format(self.d_packets_counts["Others"]))
                    ## 更新包数量列表 End

                # 更新组件
                pass
                # listbox.update_idletasks()

    def _initialize_menu(self, frame):
        buttons = OrderedDict()

        # 创建各种按钮
        buttons["start"] = tkinter.Button(frame, text="Start capturing packets", fg="red", command=None)
        buttons["stop"] = tkinter.Button(frame, text="Stop capturing packets", fg="blue", command=None)
        buttons["restart"] = tkinter.Button(frame, text="Restart current capture", fg="orange", command=None)
        buttons["options"] = tkinter.Button(frame, text="Capture options", fg="green", command=None)

        # 放置控件
        column = 0
        for each_button in buttons:
            buttons[each_button].grid(row=0, column=column)
            column += 1
        frame.pack()

    def _initialize_root(self, root):
        # 设置窗口大小
        root.geometry("800x640")

        # 设置标题
        root.title("Sniffer By w@tch")

        # 不允许更改窗口大小
        root.resizable(height=False, width=False)

    def _initialize_content_frame(self, frame):
        # 图形化显示/其余功能选项帧
        functions_listbox = tkinter.Listbox(frame)
        functions_listbox.pack(side=tkinter.LEFT, fill=tkinter.Y)

        ## 内容显示帧 Start
        content_width = 90
        content_frame = tkinter.LabelFrame(frame)

        # 十六进制帧 Start
        hex_text_frame = tkinter.LabelFrame(content_frame)
        self.hex_text = tkinter.Text(hex_text_frame, width=content_width, height=10)
        self.hex_text.configure(state="disabled")  # 使得用户无法输入
        self.hex_text.grid()
        hex_text_frame.pack(side=tkinter.BOTTOM, fill=tkinter.Y)
        # 十六进制帧 End

        # 包内容详细打印 Start
        contents_text_frame = tkinter.LabelFrame(content_frame)
        self.contents_text = tkinter.Text(contents_text_frame, width=content_width, height=10)
        self.contents_text.configure(state="disabled")  # 使得用户无法输入
        self.contents_text.grid()
        contents_text_frame.pack(side=tkinter.TOP, fill=tkinter.Y)
        # 包内容详细打印 End

        content_frame.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        ## 内容显示帧 End

        frame.pack()

    def _initialize_packets_area_labels(self, frame):
        labels = dict()
        label_width = 8

        # justify与anchor的区别了：一个用于控制多行的对齐；另一个用于控制整个文本块在Label中的位置
        labels["0"] = tkinter.Label(frame, text="序号", anchor="w", width=label_width)
        labels["1"] = tkinter.Label(frame, text="包概要", anchor="w", width=label_width * 9)

        for label in labels:
            labels[label].grid(row=0, column=int(label))

        frame.grid(row=0, column=0, columnspan=len(labels))

    def handlerAdaptor(self, fun, **kwds):
        # 参考 http://blog.csdn.net/tinym87/article/details/6957438
        '''事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧'''
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

    @staticmethod
    def _hexdump(x):
        """
        改造 scapy.utils 库中的 hexdump 为我所用(NND 的库函数要是跟写个返回值我就不用手改了)
        还有另外一种方式,参考 show() 函数,直接打印到字符串了
        :param x:
        :return:
        """
        result = ""
        if type(x) is not str and type(x) is not bytes:
            try:
                x = bytes(x)
            except:
                x = str(x)
        l = len(x)
        i = 0
        while i < l:
            result += "%04x  " % i + " "
            for j in range(16):
                if i + j < l:
                    result += "%02X" % orb(x[i + j]) + " "
                else:
                    result += "  " + " "
                if j % 16 == 7:
                    result += "" + " "
            result += " " + " "
            result += sane_color(x[i:i + 16]) + "\n"
            i += 16
        return result

    def _print_packet_contents(self, event, listbox):
        packet = self.l_packets[listbox.curselection()[0]]
        hex_contents = MyUI._hexdump(packet)

        ## 十六进制面板 Start
        # state="normal",使得我们可以输入内容, 输完内容后改 state 为 disabled 使用户无法输入
        self.hex_text.configure(state="normal")
        self.hex_text.delete("1.0", tkinter.END)  # 清空原先的内容
        self.hex_text.insert(tkinter.END, hex_contents)
        self.hex_text.configure(state="disabled")
        ## 十六进制面板 End

        ## 包详细内容面板 Start
        # 将 show 结果 print 打印到字符串, 重定向 stdout 到字符串
        with io.StringIO() as buf, redirect_stdout(buf):
            packet.show()
            show_str = buf.getvalue()

        self.contents_text.configure(state="normal")
        self.contents_text.delete("1.0", tkinter.END)  # 清空原先的内容
        self.contents_text.insert(tkinter.END, show_str)
        self.contents_text.configure(state="disabled")
        ## 包详细内容面板 End

    def _initialize_packets_area_listbox(self, frame):
        packets_list_box = tkinter.Listbox(frame, width=80)

        # 给 listbox 组件添加滚动条
        scrollbar = tkinter.Scrollbar(frame)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        packets_list_box.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=packets_list_box.yview)

        # 更新包的线程
        packets_update_thread = threading.Thread(target=self._update_packets_list, args=(packets_list_box,))
        packets_update_thread.start()

        # 单击后就显示内容
        packets_list_box.bind('<Double-Button-1>',
                              self.handlerAdaptor(self._print_packet_contents, listbox=packets_list_box))

        packets_list_box.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        frame.grid(row=1)

    def _initialize_list_frame(self, frame):
        ## 包数量列表 Start TODO: 本来想写成 IP 列表的, 待定
        self.packets_num_listbox = tkinter.Listbox(frame)
        self.packets_num_listbox.pack(side=tkinter.LEFT, fill=tkinter.Y)
        ## 包数量列表 End

        ## 包 区域 Start
        packets_area_frame = tkinter.LabelFrame(frame)

        # 标签帧 Start
        labels_frame = tkinter.LabelFrame(packets_area_frame)
        self._initialize_packets_area_labels(labels_frame)
        # 标签帧 End

        # 包列表帧 Start
        packets_frame = tkinter.Frame(packets_area_frame)
        self._initialize_packets_area_listbox(packets_frame)
        # 包列表帧 End

        packets_area_frame.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        ## 包 区域 End

        frame.pack()


if __name__ == "__main__":
    ui = MyUI()
