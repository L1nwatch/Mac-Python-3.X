#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
'''
多进程版本,发现不太好共享变量,所以还是全部改写成多线程好了
用于实现嗅探器的 UI 界面, 本来想用 PyQt 写的, 但是还没学, 而且时间不够, 所以还是用 tkinter 实现了
突然发现 LabelFrame 比 Frame 好看些, 至少在 Mac 下是的(至少在我的审美观下是的)
Python 多线程居然不支持线程挂起的, 幸好我学了操作系统, 用互斥量解决了- -
'''
__author__ = '__L1n__w@tch'

# TODO: 列出监测主机的所有网卡，选择一个网卡，设置为混杂模式进行监听
# TODO: 捕获所有流经网卡的数据包，并利用WinPcap函数库设置过滤规则
# (报告)TODO: 将所开发工具的捕获和分析结果与常用的Sniffer进行比较，完善程序代码
# TODO: 以太网帧格式等
# TODO: IGMP
# TODO: 所开发的嗅探工具能够根据协议类型、端口、地址等信息对数据包进行过滤
# TODO: 实验报告要求
# TODO: 在实验报告中写出程序关键算法和流程图
# TODO: 根据WinPcap常用库函数总结出基于WinPcap的嗅探器的程序框架
# TODO: 阐述碰到的问题以及解决方法
# TODO: 阐述收获与体会
# TODO: 并附上程序界面和运行结果


import tkinter
import sys
import threading
import io
import tkinter.messagebox as mb
from contextlib import redirect_stdout
from collections import OrderedDict
from my_sniffer import MySnifferThread, l_packets
from scapy.utils import sane_color, orb


class MyUI:
    def __init__(self):
        global l_packets
        self.d_packets_counts = {"TCP": 0, "UDP": 0, "ICMP": 0, "ARP": 0, "Others": 0, "Total": 0}
        self.d_configuration = OrderedDict()
        self.d_configuration["TCP"], self.d_configuration["UDP"], self.d_configuration["ICMP"], self.d_configuration[
            "ARP"], self.d_configuration["Others"] = True, True, True, True, True

        # 嗅探线程
        self.my_sniffer_thread = MySnifferThread()

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
        self.d_packets_counts["Total"] += 1

    def _update_packets_num_listbox(self):
        self.packets_num_listbox.delete(0, tkinter.END)
        self.packets_num_listbox.insert(tkinter.END, "TCP:{}".format(self.d_packets_counts["TCP"]))
        self.packets_num_listbox.insert(tkinter.END, "UDP:{}".format(self.d_packets_counts["UDP"]))
        self.packets_num_listbox.insert(tkinter.END, "ICMP:{}".format(self.d_packets_counts["ICMP"]))
        self.packets_num_listbox.insert(tkinter.END, "ARP:{}".format(self.d_packets_counts["ARP"]))
        self.packets_num_listbox.insert(tkinter.END, "Others:{}".format(self.d_packets_counts["Others"]))
        self.packets_num_listbox.insert(tkinter.END, "Total:{}".format(self.d_packets_counts["Total"]))

    def _update_packets_list(self, listbox):
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
                    self._update_packets_num_listbox()
                    ## 更新包数量列表 End
                    # listbox.update_idletasks()# 更新组件

    def _stop_sniff_thread(self):
        res = self.my_sniffer_thread.is_stopped()
        if res is True:
            tkinter.messagebox.showerror(title="Stop capturing packets", message="嗅探早就停止了")
        elif res is False:
            self.my_sniffer_thread.stop()
            tkinter.messagebox.showinfo(title="Stop capturing packets", message="停止嗅探ing, 可以按 Restart 继续嗅探")
            self.buttons["restart"].configure(state="normal")
        elif res is None:
            tkinter.messagebox.showerror(title="Stop capturing packets", message="并没有嗅探过")

    def _lfilter_func(self, packet):
        """
        根据 self.d_configuration, 配置 sniff 所需要的 lfilter 函数
        :return:
        """
        for protocol in self.d_configuration:
            if protocol != "Others":
                if packet.haslayer(protocol) and not self.d_configuration[protocol]:
                    return False
            elif self.d_configuration["Others"]:
                return True
        return True

    def _start_sniff_thread(self):
        # TODO: 为了减小本人的工作量, 只允许进行一次配置, 且只能在没开始嗅探之前配置...
        self.buttons["options"].configure(state="disabled")

        self.my_sniffer_thread.configuration(lfilter=self._lfilter_func)
        self._initialize_functions_listbox()

        self.my_sniffer_thread.start()
        self.buttons["start"].configure(state="disabled")  # 使得按钮无法再按

    def _restart_sniff_thread(self):
        self.my_sniffer_thread.restart()
        self.buttons["restart"].configure(state="disabled")

    def _checkbutton_callback(self, protocol):
        """
        功能是实现配置选项, 如果选中变为未选中,则令对应配置值变为 False
        例如, 原来 self.d_configuration["TCP"] = True, 执行完这个函数之后, self.d_configuration["TCP"] = False
        :param protocol: "TCP"
        :return:
        """
        self.d_configuration[protocol] = not self.d_configuration[protocol]

    def _initialize_packets_filter_buttons(self, frame):
        """
        初始化配置窗口中的过滤器中的包类型
        :param frame: 包选择过滤帧
        :return:
        """
        self.checkbuttons = OrderedDict()

        self.checkbuttons["TCP"] = tkinter.Checkbutton(frame, text="TCP",
                                                       command=lambda: self._checkbutton_callback("TCP"))
        self.checkbuttons["UDP"] = tkinter.Checkbutton(frame, text="UDP",
                                                       command=lambda: self._checkbutton_callback("UDP"))
        self.checkbuttons["ICMP"] = tkinter.Checkbutton(frame, text="ICMP",
                                                        command=lambda: self._checkbutton_callback(
                                                            "ICMP"))
        self.checkbuttons["ARP"] = tkinter.Checkbutton(frame, text="ARP",
                                                       command=lambda: self._checkbutton_callback("ARP"))
        self.checkbuttons["Others"] = tkinter.Checkbutton(frame, text="Others",
                                                          command=lambda: self._checkbutton_callback(
                                                              "Others"))

        for each_button in self.checkbuttons:
            if self.d_configuration[each_button]:
                self.checkbuttons[each_button].select()  # 默认为选中状态
            else:
                self.checkbuttons[each_button].deselect()  # 未选中状态
            self.checkbuttons[each_button].pack()

    def _configure_options(self):
        # 通过子窗口来进行配置
        sub_window = tkinter.Toplevel()
        sub_window.title("配置窗口")

        ## 包过滤选择帧 Start
        packets_filter_labelframe = tkinter.LabelFrame(sub_window)

        checkbutton_label = tkinter.Label(packets_filter_labelframe, text="选择所要保留的包类型", anchor="w")
        checkbutton_label.pack()
        # 初始化几个复选框
        self._initialize_packets_filter_buttons(packets_filter_labelframe)

        packets_filter_labelframe.pack()
        ## 包过滤选择帧 End

        sub_window.grid()

    def _initialize_menu(self, frame):
        self.buttons = OrderedDict()

        # 创建各种按钮
        self.buttons["start"] = tkinter.Button(frame, text="Start capturing packets", fg="red",
                                               command=self._start_sniff_thread)
        self.buttons["stop"] = tkinter.Button(frame, text="Stop capturing packets", fg="blue",
                                              command=self._stop_sniff_thread)
        self.buttons["restart"] = tkinter.Button(frame, text="Restart current capture", fg="orange", state="disabled",
                                                 command=self._restart_sniff_thread)
        self.buttons["options"] = tkinter.Button(frame, text="Capture options", fg="green",
                                                 command=self._configure_options)

        # 放置控件
        column = 0
        for each_button in self.buttons:
            self.buttons[each_button].grid(row=0, column=column)
            column += 1
        frame.pack()

    def _initialize_root(self, root):
        # 设置窗口大小
        root.geometry("800x640")

        # 设置标题
        root.title("Sniffer By w@tch")

        # 不允许更改窗口大小
        root.resizable(height=False, width=False)

    def _initialize_functions_listbox(self):
        # TODO: 本来想写成功能区的,暂时没时间,所以写成配置显示区好了
        self.functions_listbox.delete(0, tkinter.END)
        for protocol in self.d_configuration:
            self.functions_listbox.insert(tkinter.END, "{}:{}".format(protocol, self.d_configuration[protocol]))

    def _initialize_content_frame(self, frame):
        # 图形化显示/其余功能选项帧
        self.functions_listbox = tkinter.Listbox(frame)
        self.functions_listbox.pack(side=tkinter.LEFT, fill=tkinter.Y)

        ## 内容显示帧 Start
        content_width = 90
        content_frame = tkinter.LabelFrame(frame)

        # 十六进制帧 Start
        hex_text_frame = tkinter.LabelFrame(content_frame)
        self.hex_text = tkinter.Text(hex_text_frame, width=content_width, height=10)
        self.hex_text.bind("<1>", lambda event: self.hex_text.focus_set())  # 使之变为可读且可复制
        self.hex_text.configure(state="disabled")  # 使得用户无法输入
        self.hex_text.grid()
        hex_text_frame.pack(side=tkinter.BOTTOM, fill=tkinter.Y)
        # 十六进制帧 End

        # 包内容详细打印 Start
        contents_text_frame = tkinter.LabelFrame(content_frame)
        self.contents_text = tkinter.Text(contents_text_frame, width=content_width, height=10)
        self.contents_text.bind("<1>", lambda event: self.contents_text.focus_set())  # 使之变为可读且可复制
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
        # 增加一个按钮,要不然实在得自己滚到最底,不方便
        button = tkinter.Button(frame, text="滑至底部", command=lambda: self.packets_listbox.yview(tkinter.END))

        for label in labels:
            labels[label].grid(row=0, column=int(label))

        button.grid(row=0, column=len(labels) - 1)
        frame.grid(row=0, column=0, columnspan=len(labels))

    def _handler_adaptor(self, fun, **kwds):
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
        self.packets_listbox = tkinter.Listbox(frame, width=80)

        # 给 listbox 组件添加滚动条
        scrollbar = tkinter.Scrollbar(frame)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.packets_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.packets_listbox.yview)

        # 更新包的线程
        packets_update_thread = threading.Thread(target=self._update_packets_list, args=(self.packets_listbox,))
        packets_update_thread.start()

        # 单击后就显示内容
        self.packets_listbox.bind('<Double-Button-1>',
                                  self._handler_adaptor(self._print_packet_contents, listbox=self.packets_listbox))

        self.packets_listbox.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        frame.grid(row=1)

    def _initialize_list_frame(self, frame):
        ## 包数量列表 Start TODO: 本来想写成 IP 列表的, 待定
        self.packets_num_listbox = tkinter.Listbox(frame)
        self.packets_num_listbox.pack(side=tkinter.LEFT, fill=tkinter.Y)
        self._update_packets_num_listbox()
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
