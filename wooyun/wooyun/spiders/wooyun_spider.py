#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from wooyun.items import  WooyunItem
import re

class WooyunSpider(Spider):
    name = "wooyun" 
    allowed_domains = ["wooyun.org"]
    start_urls=["http://www.wooyun.org/bugs/new_public"]
    #减慢爬取速度
    #download_delay = 1

    def __init__(self):
        #fixme:从数据库中读取数据总数,历史总数等数据，判断本次爬取数据数量及起始点
        self.__local_counts = 0
        self.__old_counts = 0
        self.__now_counts = 0



    def parse(self , response):
        #获取页面数量
        page_counts = response.selector.xpath("//p[@class='page']/text()").re("\d+")[1]
        #获取记录数量
        self.__now_counts = response.selector.xpath("//p[@class='page']/text()").re("\d+")[0]

        #fixme:加判断是否继续
        for page_index in range(1,int(page_counts)+1):
        #for page_index in range(1,2):  #for test
            list_url = response.urljoin(r"/bugs/new_public/page/" + str(page_index))
            yield Request(list_url, callback = self.parse_list)

          

     #解析漏洞列表页面
    def parse_list(self, response):
        article_urls =  response.selector.xpath('//table/tbody/tr/td/a/@href').extract()
        for article_url in article_urls:	
            article_url = "http://www.wooyun.org"+article_url
            #fixme:加判断是否继续
            yield Request(article_url,callback = self.parse_article)
        #yield Request("http://www.wooyun.org/bugs/wooyun-2015-0131337",callback = self.parse_article)


    #解析漏洞信息页面
    def parse_article(self , response):
        item = WooyunItem()
        sel = Selector(response)
        item['bug_title'] = sel.xpath("//h3[@class='wybug_title']/text()").extract()[0].replace('\t','').split('：')[1]
        item['open_date'] = sel.xpath("//h3[@class='wybug_date']/text()").re("[\d+]{4}-[\d+]{2}-[\d+]{2} [\d+]{2}:[\d+]{2}")[0]
        item['bug_type'] = sel.xpath("//h3[@class='wybug_type']/text()").extract()[0].replace('\t', '').split('：')[1]
        #item['bug_id'] = sel.xpath("//div[@class='content']/h3/a[contains(@href,'bugs/wooyun')]/text()").extract()[0]
        item['bug_id'] = response.url.split('/')[4] 
        item['author'] =  sel.xpath("//h3[@class='wybug_author']/a/text()").extract() [0]
        item['html'] = sel.xpath('/*').extract()[0]
        item['image_urls'] = sel.xpath("//img[contains(@src, 'http://static.wooyun.org/wooyun/upload/')]/@src").extract()
        return item
        #print response.body	