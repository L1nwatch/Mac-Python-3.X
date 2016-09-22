# 网络对抗原理-嗅探器

## 说明

这主要是课堂上的任务，要求实现嗅探器，而且还要写带有图形界面的，主要使用了 scapy 库还有 tkinter 库还写图形界面，具体的还是看代码吧。

## 最终实现

最终在自己的 macOS 运行的截图如下所示，由于 Python 是跨平台的，所以在其他平台运行差异也许不大，不过自己没有测试过：

![macOS 运行嗅探器截图](https://github.com/L1nwatch/Mac-Python-3.X/blob/master/%E7%BD%91%E7%BB%9C%E5%AF%B9%E6%8A%97%E5%8E%9F%E7%90%86/%E6%BC%94%E7%A4%BA%E7%A4%BA%E4%BE%8B.png?raw=true)

### PS

这个嗅探器自己平常用不到（我又不干坏事，再说干坏事至少也要拿 WireShark 那种级别的啊。。。），所以代码好久没有维护了，使用的方法大致是：

`python3.4 sniffer/submit/sniff_ui_threading.py `，这个是封装好的用户界面类，直接使用这个就可以了。

具体文档可以参考放在百度文库的[报告](http://wenku.baidu.com/view/d364978c25c52cc58bd6befb)。

