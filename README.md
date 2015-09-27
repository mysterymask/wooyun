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
* 按路径建立文件夹：wooyun/web/app/static/wooyun_res/htmls、wooyun/web/app/static/wooyun_res/images
* 在wooyun/下运行默认命令：scrapy crawl wooyun，完成所有数据的爬取。有三个参数可控制爬取方式。
  
  **-a page_max:**控制爬取页数。0：默认值，表示全部爬取；num：大于0，表示爬取页数。**eg:scrapy crawl -a page_max=2 wooyun** #爬取两页数据(即第一页和第二页)

  **-a local_store:**控制是否将页面及图片下载至本地。true：默认值，下载页面和图片至本地保存；false：不下载页面和图片，只保存标题等信息及相关链接。 **eg:scrapy crawl -a local_store=true wooyun**
  
  **-a update:**控制是否为增量更新爬取。false：默认值，非增量更新爬取（全部爬取）；ture：增量爬取，从之前的爬取位置起从后向前爬取。**eg:scrapy crawl -a update=true wooyun**

* 爬虫参数保存位置为：wooyun/wooyun/spider/settings.py，可根据需要修改
* web参数保存位置为：wooyun/web/app/views_py/settings.py

###3.爬取乌云知识库
* 按路径建立文件夹：wooyun/web/app/static/wooyun_res/htmls、wooyun/web/app/static/wooyun_res/images
* 在wooyuh/下运行默认命令：scrapy runspider wooyun/spider/wooyun_doc_spider.py，完成所有数据爬取。有两个参数控制爬取方式。

  **-a page_max:**控制爬取页数。0：默认值，表示全部爬取；num：大于0，表示爬取页数。**eg:scrapy runspider  -a page_max=2 wooyun/spider/wooyun_doc_spider.py** #爬取两页数据(即第一页和第二页)

  **-a local_store:**控制是否将页面及图片下载至本地。true：默认值，下载页面和图片至本地保存；false：不下载页面和图片，只保存标题等信息及相关链接。 **eg:scrapy runspider -a local_store=true wooyun/spider/wooyun_doc_spider.py**
  
* 由于页面没有知识库文章总量参数，因此无法通过数量判断更新量，更新时需手动输入参数。

###4.web信息搜索

web界面采用Flask框架作为web服务器，bootstrap作为前端

启动web server ：在web目录下运行python run.py，默认端口是5000

搜索：在浏览器通过http://localhost:5000进行搜索漏洞，多个关键字可以用空格分开。

###5.其它

本程序只用于技术研究和个人使用，程序组件均为开源程序，漏洞来源于乌云公开漏洞，版权归wooyun.org

mysterymask@163.com
