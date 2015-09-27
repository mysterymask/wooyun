# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WooyunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    now_counts = scrapy.Field() #网站当前记录总量

    bug_title = scrapy.Field() #漏洞标题
    open_date = scrapy.Field() #公开时间
    bug_type = scrapy.Field() #漏洞类型
    bug_id = scrapy.Field() #缺陷编号
    author = scrapy.Field() #作者
    html = scrapy.Field() #详细内容
    
    image_urls = scrapy.Field()  #图片路径
    images = scrapy.Field() #已下载的图片

    content_type = scrapy.Field()
    local_store_flag = scrapy.Field()