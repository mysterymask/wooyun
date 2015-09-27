#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.conf import settings
from wooyun.items import  WooyunItem
import pymongo
import re
import math

class WooyunSpider(Spider):
    name = "wooyun" 
    allowed_domains = ["wooyun.org"]
    start_urls=["http://drops.wooyun.org/"]
    #减慢爬取速度
    #download_delay = 0.1

    def __init__(self,page_max=settings['PAGE_MAX_DEFAULT'],local_store=settings['LOCAL_STORE_DEFAULT'] ):

        self.db_client = pymongo.MongoClient(settings['DB_HOST'],settings['DB_PORT'])
        self.db_database = self.db_client[settings['DB_DATABASE']]
        #self.__db_database.authenticate('wooyun','wooyun')
        self.db_collection = self.db_database[settings['DB_COLLECTION_DOC']]
        self.page_max = int(page_max)
        self.local_store_flag = 'true' == local_store.lower()


    def closed(self,reason):
        self.db_client.close()


    def parse(self , response):
        #获取页面数量
        page_counts = int(response.selector.xpath("//span[@class='pages']/text()").re(u'共.(\d+).页')[0])

        page_end = 0
        page_start = page_counts

        if self.page_max > 0:
            page_start = min(self.page_max,page_counts)

        for page_index in range(1,2): #for test
        #for page_index in range(page_end,page_start): 
            list_url = response.urljoin(r"page/" + str(page_index))
            #print list_url
            yield Request(list_url, callback = self.parse_list)

          

     #解析漏洞列表页面
    def parse_list(self, response):
        article_urls =  response.selector.xpath("//div/h2[@class='entry-title']/a/@href").extract()
        for article_url in article_urls:	
            article_id = article_url.split('/')[4]
            if self.is_in_db(article_id) == False:
                yield Request(article_url,callback = self.parse_article)
                #print article_url
      


    #解析漏洞信息页面
    def parse_article(self , response):
        item = WooyunItem()
        sel = Selector(response)
        item['bug_title'] = sel.xpath("//h1[@class='entry-title ng-binding']/text()").extract()[0]
        item['open_date'] = sel.xpath("//div[@class='entry-meta']/time/text()").re("[\d+]{4}/[\d+]{2}/[\d+]{2} [\d+]{2}:[\d+]{2}")[0]
        item['bug_type'] = "知识库"
        item['bug_id'] = response.url.split('/')[4] 
        #item['author'] =  sel.xpath("//h3[@class='wybug_author']/a/text()").extract() [0]
        item['author'] = sel.xpath("//div[@class='entry-meta']/a/@href").extract()[0].split('/')[2]
        item['html'] = sel.xpath('/*').extract()[0]
        #print "self.local_store_flag:" + self.local_store_flag
        if self.local_store_flag:
            item['image_urls'] = sel.xpath("//img[contains(@src,'http://static.wooyun.org//drops')]/@src").extract()
        else:
            item['image_urls'] = []
        item['local_store_flag'] = self.local_store_flag
        item['content_type'] = 'wooyun_doc'
        return item	

    def get_local_reords_count(self):
        rexExp = re.compile('', re.IGNORECASE)
        res =  self.db_collection.find({'$or':[{'bug_title':rexExp},{'author':rexExp},{'bug_id':rexExp},{'bug_type':rexExp},{'open_date':rexExp}]})
        return res.count()

    def is_in_db(self,wy_id):        
        wooyun_id_exsist = True if self.db_collection.find({'bug_id':wy_id}).count()>0 else False
        return wooyun_id_exsist
  