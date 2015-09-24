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
    start_urls=["http://www.wooyun.org/bugs/new_public"]
    #减慢爬取速度
    #download_delay = 1

    def __init__(self,page_max=settings['PAGE_MAX_DEFAULT'],local_store=settings['LOCAL_STORE_DEFAULT'],update=settings['UPDATE_DEFAULT'] ):

        self.db_client = pymongo.MongoClient(settings['DB_HOST'],settings['DB_PORT'])
        self.db_database = self.db_client[settings['DB_DATABASE']]
        #self.__db_database.authenticate('wooyun','wooyun')
        self.db_collection = self.db_database[settings['DB_COLLECTION']]
        self.local_counts = self.get_local_reords_count()
        self.update_flag = 'true' == update.lower()
        self.page_max = int(page_max)
        self.local_store_flag = 'true' == local_store.lower()


    def closed(self,reason):
        self.db_client.close()


    def parse(self , response):
        #获取页面数量
        page_counts = int(response.selector.xpath("//p[@class='page']/text()").re("\d+")[1])
        #获取记录数量
        self.total_counts = int(response.selector.xpath("//p[@class='page']/text()").re("\d+")[0])

        if self.update_flag :
            page_counts = int(math.ceil((self.total_counts - self.local_counts)/(settings['RECORDS_PER_PAGE']*1.0)))

        page_end = 0
        page_start = page_counts
        if self.page_max > 0 and self.update_flag:
            page_end = page_counts - min(page_counts,self.page_max)
        if self.page_max > 0 and self.update_flag == False:
            page_start = self.page_max

        for page_index in range(page_start,page_end,-1): 
            list_url = response.urljoin(r"/bugs/new_public/page/" + str(page_index))
            yield Request(list_url, callback = self.parse_list)

          

     #解析漏洞列表页面
    def parse_list(self, response):
        article_urls =  response.selector.xpath('//table/tbody/tr/td/a/@href').extract()
        for article_url in article_urls:	
            wy_id = article_url.split('/')[2]
            if self.is_in_db(wy_id) == False:
                article_url = "http://www.wooyun.org"+article_url
                yield Request(article_url,callback = self.parse_article)
      


    #解析漏洞信息页面
    def parse_article(self , response):
        item = WooyunItem()
        sel = Selector(response)
        item['bug_title'] = sel.xpath("//h3[@class='wybug_title']/text()").extract()[0].replace('\t','').split('：')[1]
        item['open_date'] = sel.xpath("//h3[@class='wybug_open_date']/text()").re("[\d+]{4}-[\d+]{2}-[\d+]{2} [\d+]{2}:[\d+]{2}")[0]
        item['bug_type'] = sel.xpath("//h3[@class='wybug_type']/text()").extract()[0].replace('\t', '').split('：')[1]
        item['bug_id'] = response.url.split('/')[4] 
        #item['author'] =  sel.xpath("//h3[@class='wybug_author']/a/text()").extract() [0]
        item['author'] = sel.xpath("//h3[@class='wybug_author']/a/@href").extract()[0].split('/')[4]
        item['html'] = sel.xpath('/*').extract()[0]
        if self.local_store_flag:
            item['image_urls'] = sel.xpath("//img[contains(@src, 'http://static.wooyun.org/wooyun/upload/')]/@src").extract()
        else:
            item['image_urls'] = []
        item['local_store_flag'] = self.local_store_flag
        return item	

    def get_local_reords_count(self):
        rexExp = re.compile('', re.IGNORECASE)
        res =  self.db_collection.find({'$or':[{'bug_title':rexExp},{'author':rexExp},{'bug_id':rexExp},{'bug_type':rexExp},{'open_date':rexExp}]})
        return res.count()

    def is_in_db(self,wy_id):        
        wooyun_id_exsist = True if self.db_collection.find({'bug_id':wy_id}).count()>0 else False
        return wooyun_id_exsist
  