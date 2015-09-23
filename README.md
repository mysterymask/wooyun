#wooyun爬虫及搜索

**wooyun.org bug search**

![index.html](https://github.com/mysterymask/wooyun/blob/master/wooyun/index.png)

![list.html](https://github.com/mysterymask/wooyun/blob/master/wooyun/list.png)

###1.相关组件

Python (建议2.7)  pip</br>
mongodb</br>
scrapy</br>
Flask</br>
pymongo</br>

###2.爬取wooyun公开漏洞

在wooyun/下运行scrapy crawl wooyun

目前是爬取全部信息,后续将增加增量爬取 断点续传等功能


###3.web信息搜索

web界面采用Flask框架作为web服务器，bootstrap作为前端

启动web server ：在web目录下运行python run.py，默认端口是5000

搜索：在浏览器通过http://localhost:5000进行搜索漏洞，多个关键字可以用空格分开。

###4.其它

本程序只用于技术研究和个人使用，程序组件均为开源程序，漏洞来源于乌云公开漏洞，版权归wooyun.org

mysterymask@163.com
