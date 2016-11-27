## 说明

本工具用于公司内部案例平台的爬取，由于所有案例都是在页面上操作，而且页面没有提供查询功能，所以自己写了一个爬虫来把所有案例 download 到本地，进而可以实现一些页面上实现不了的操作，比如搜索指定关键字等。

* 本程序采用 TDD 开发，但是发现写这种 C/S 架构的功能测试和单元测试有点区分不开，至少没有之前写 B/S 架构的那么分明

## 程序使用截图

* 命令行执行，指定 url 还有路径即可，路径默认为同目录，url 则必须指定：

![开始爬行](https://github.com/L1nwatch/Mac-Python-3.X/blob/master/ATM%E6%A1%88%E4%BE%8B%E7%88%AC%E8%99%AB/%E5%BC%80%E5%A7%8B%E7%88%AC%E8%A1%8C.png?raw=true)

![爬行结束](https://github.com/L1nwatch/Mac-Python-3.X/blob/master/ATM%E6%A1%88%E4%BE%8B%E7%88%AC%E8%99%AB/%E7%88%AC%E8%A1%8C%E7%BB%93%E6%9D%9F.png?raw=true)