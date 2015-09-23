# -*- coding: utf-8 -*-

# Scrapy settings for wooyun project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'wooyun'

SPIDER_MODULES = ['wooyun.spiders']
NEWSPIDER_MODULE = 'wooyun.spiders'


ITEM_PIPELINES = {
    'wooyun.pipelines.WooyunPipeline':800,
    'scrapy.contrib.pipeline.images.ImagesPipeline': 1
}

IMAGES_STORE = 'web/app/static/wooyun_res/images'
LOCAL_HTML_STORE = 'web/app/static/wooyun_res/htmls/'

#DB_HOST = "172.18.85.121"
DB_HOST = '192.168.1.133'
DB_PORT = 27017
DB_DATABASE = "wooyun"
DB_COLLECTION = "wooyun_list"

LOCAL_IMAGES_STORE = '../images/'
LOCAL_CSS_PATH = "../../css/style.css"
LOCAL_JS_PATH =  "../../js/jquery-1.4.2.min.js"  

PAGE_MAX_DEFAULT = 0
LOCAL_STORE_DEFAULT = 'true'
UPDATE_DEFAULT = 'false'
RECORDS_PER_PAGE = 20