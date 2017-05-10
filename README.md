# Mac Python 3.X
* Start From 2016.02
* Write Python in Mac OS X(10.10.5)
* Python 3.4
* IDLE: PyCharm

# Description
保存自己平常做的小作品，单独弄一个 git 不合适，就整合到一起了

```shell
# 更新
2017.05.10 完善当链接数过多时的关系链接库统计代码
2017.05.09 补充完成分析数据库脚本、创建数据库脚本, 完善真实数据库与伪造数据库的一致性
2017.05.06 修改评测的测试代码, 使其兼容最新的链接关系库、新增伪造链接的相关统计代码, 方便伪造控制、完成 MRR 和 precision 流程的全部计算工作
2017.05.05 完善毕设数据库脚本, 实现了链接关系库的伪造工作(说得好义正言辞啊= =)
2017.04.28 写了个脚本, 用于从 LaTex 源码文件中提取正文内容(自动删除标签、引用等)
2017.03.18 完善 xml2json, 增加全角字符的处理操作
2017.03.17 继续完善 xml2json, 主要是区分 demo 和完整版数据
2017.03.16 修正 wifi 名称错误, 另外给 xml2json 增加两步不可读字符的处理操作
2017.03.15 新增一个 xml2json 的小工具, 主要是针对自己毕设用的, 用于转换搜狗实验室源为 json 数据以便 Lucene 建立索引
2017.03.14 新增一键开关内网穿透的功能到自己的集成工具箱里
```

## 作品清单(2017-02-15)

### 本仓库内

####  ATM 编码转换工具

涉及 tkinter UI 开发、re 库、`unicode_escape` 编码，主要用于处理公司 ATM 平台显示日志信息乱码的问题，提供一个 UI 界面便于使用者操作

####  ATM 案例爬虫

涉及 MySQL 数据库操作，命令行交互 argparse 库，requests HTTP 库实现爬虫，re 匹配，自定义 const 常量类等。主要是爬取 ATM 平台的自动化测试案例到本地，方便搜寻，另外后期打算基于这个做一个能提供类似于 svn 跟踪案例以及回滚案例编写的平台

#### ATM 结果提取工具

涉及 requests HTTP 库、PyQt5 UI 开发。主要是给自动化负责人报告执行结果的时候，每次都有重复冗余的人工操作，于是干脆用脚本来实现自动化了，并且提供了 UI 界面方便整理结果报告。

#### 毕设辅助脚本

##### xml转json

毕设需要使用搜狗的数据源, 然而搜狗数据源是一大堆内容都放在同一个 txt 里面的, 格式是类似于 xml 格式, 但是没法直接用 xml 库解析, 而且自己本身的毕设是基于 JSON, 所以干脆弄了个脚本来把 xml 文本转成 json 文本, 还有域名解析统计等操作, 方便评测用的

##### SQLite数据库辅助

采用 peewee 库实现的, 创建一个链接关系数据库, 源是搜狗数据源(后期改为自己随机创建数据), 然后保存到 sqlite3 db 文件里面, 方便 Java 读取

##### 评测

要求进行查准率以及 MRR 的评测工作, 于是开始使用 selenium 库进行相关的自动化操作并计算评测结果

##### LaTex 正文内容提取工具

查重的时候要求提交正文内容, 正式的查重可以用 pdf, 不过我看 paperpass 只能用文本或者 docx, 所以还是写个脚本来把正文内容提取出来吧

#### NTester 规则生样本

涉及 scapy 库解析 pcap 包，构造 DNS 数据包，requests HTTP 库，正则 re 库，sqlite3 数据库处理，DES 加密，PKCS#5 填充，命名元组，paramiko 库进行 SSH 连接，json 文件读写，SVN 库交互，解压 gz、tar 包等。是公司一款测试产品的附加组件，给 NTester 规则库提供升级样本用的。

#### [文件内容搜索器](https://github.com/L1nwatch/Mac-Python-3.X/blob/master/%E6%96%87%E4%BB%B6%E5%86%85%E5%AE%B9%E6%90%9C%E7%B4%A2%E5%99%A8/readme.md)

使用说明详看链接，涉及 os、argparse、chardet、re、platform 等库。主要是进行文件内容的搜索功能，类似于 macOS 的 Spotlight 搜索，不过可以指定路径，以及搜索的路径等。近期在考虑给这个加上一层 UI 界面方便操作。

#### [本地文件夹同步器](https://github.com/L1nwatch/Mac-Python-3.X/blob/master/%E6%9C%AC%E5%9C%B0%E6%96%87%E4%BB%B6%E5%A4%B9%E5%90%8C%E6%AD%A5%E5%99%A8/README.md)

使用说明详看链接，同样涉及 os 等库。主要是进行本地两个文件夹的自动同步用的，使用场景比如，一个文件夹为日常操作，另一个文件夹为备份。

#### [网络对抗原理-嗅探器](https://github.com/L1nwatch/Mac-Python-3.X/blob/master/%E7%BD%91%E7%BB%9C%E5%AF%B9%E6%8A%97%E5%8E%9F%E7%90%86/readme.md)

详看链接，涉及 scapy、threading、io、tkinter、collections 等库。是大学课程网络对抗原理要求编写的嗅探器实验，实现了嗅探器的基本功能以及 UI 界面。

#### [自己的集成工具箱](https://github.com/L1nwatch/Mac-Python-3.X/blob/master/%E8%87%AA%E5%B7%B1%E7%9A%84%E9%9B%86%E6%88%90%E5%B7%A5%E5%85%B7%E7%AE%B1/readme.md)

详看链接，涉及 tkinter、subprocess、os、requests、random 等库。集成了各种平时需要用的小工具以及一键命令等，这样一键就能实现某个小功能，目前功能有：《开启 aria2c》、《git push 日志》、《开启 shadowsocks》、《开启或关闭 Privoxy》、《登录西电校园网》、《随机播放一集进击的巨人》、《更改隐藏文件显示状态》。

#### [计划表生成器](https://github.com/L1nwatch/Mac-Python-3.X/blob/master/%E8%AE%A1%E5%88%92%E8%A1%A8%E7%94%9F%E6%88%90%E5%99%A8/readme.md)

详看链接，涉及 datetime、calendar 库。给弟弟生成学习计划表用的。

#### [计算机网络-模拟滑窗协议](https://github.com/L1nwatch/Mac-Python-3.X/blob/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C/readme.md)

详看链接，涉及 socket、simplejson、random、argparse 等库。是课程计算机网络要求的实验作业，模拟滑动窗口协议的实现。

#### [软件安全与漏洞分析](https://github.com/L1nwatch/Mac-Python-3.X/blob/master/%E8%BD%AF%E4%BB%B6%E5%AE%89%E5%85%A8%E4%B8%8E%E6%BC%8F%E6%B4%9E%E5%88%86%E6%9E%90/readme.md)

详看链接。是课程《软件安全与漏洞分析》的实验代码，同时还有实验 153 页的实验报告。里面包含的知识点是：《堆栈溢出覆盖 SEH》、《GS 绕过》、《虚函数攻击》、《SafeSEH 绕过》、《DEP 绕过》、《ASLR 绕过》、《SEHOP 绕过》、《UAF 漏洞》、《格式化串漏洞》等。都做成了 C/S 架构，方面教学演示与学习。

#### [随机选择器](https://github.com/L1nwatch/Mac-Python-3.X/blob/master/%E9%9A%8F%E6%9C%BA%E9%80%89%E6%8B%A9%E5%99%A8/readme.md)

详看链接，主要是 random 库的进一步封装。因为自己平常有选择困难症，所以需要一个能够进行随机选择的工具。

### 其余仓库

#### [AFT 一键网管](https://github.com/L1nwatch/sangfor_tools_hub)

主要涉及 telnet 连接，cisco 命令，Django 提供 B/S 架构，实现交换机数据流监视以及开关交换机口等

#### GitBook 电子书

包括以下

*   [《Python 绝技》运用 Python 称为顶级黑客](https://github.com/L1nwatch/violent-python)


*   [《程序员健康指南》](https://github.com/L1nwatch/it_people_healthy)
*   [《ProgrammingRuby中文版第2版》](https://github.com/L1nwatch/Programming_Ruby_zhCN_gitbook)，这个还没学完
*   [《PythonWeb 开发:测试驱动开发》](https://github.com/L1nwatch/PythonWeb)
*   [《编写高质量代码改善 Python 程序的 91 个建议》](https://github.com/L1nwatch/writing_solid_python_code_gitbook)

#### [自己的网站](https://github.com/L1nwatch/my_blog_source)

实现了一键自动化部署自己的博客，其中博客的文章笔记等内容是自动同步 github 上一个专门存放笔记的库的，主要是提供笔记的搜索功能，因为目前市面上没找到自己满意的笔记搜索软件，只好自己搞一个了

#### [qlcoder](https://github.com/L1nwatch/qlcoder)

主要是存放千里码网站的练习题，还有自己给弟弟出的各种 Python 练习题，方式是让弟弟不断通过自己编写的测试来实现练习 Python 的目的

[密码学相关](https://github.com/L1nwatch/about-cryptography)

主要是自己用 Python 实现密码学相关的知识点，包括《培根编码》、《摩尔斯电码》、《栅栏密码》、《凯撒密码》等

[面试题收集整理](https://github.com/L1nwatch/interview_collect)

整理自己准备面试时的相关资料，包括 Python、C/C++、测试 等代码及知识点，已经形成 GitBook 形式了

[CTF 题收集整理](https://github.com/L1nwatch/CTF)

保存有关自己做的 CTF 题目，按 GitBook 的格式进行整理的, 所以可以用 GitBook 来进行[阅读](https://l1nwatch.gitbooks.io/ctf/content/)

[挑战 Python 网站上相关题目的代码保存](https://github.com/L1nwatch/challenge-Python)

类似于 Python 的 OJ 平台了，不过当时做的时候只支持 Python2.X 的语法，提交前可到[在线编程](http://www.pythontip.com/coding/run)进行测试