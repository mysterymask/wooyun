#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pymongo
import re
from settings import *



def search(search_params,page_index,num_per_page):
    conn = pymongo.MongoClient(DB_HOST,DB_PORT)
    db = conn[DB_NAME]
    coll = db[COLLECTION_NAME]
    rexExp = re.compile('.*'+search_params+'.*', re.IGNORECASE)
    #db.customer.find({'name':rexExp })
    #print "page_index>>>"+page_index
    start = (page_index-1) * num_per_page
    res =  coll.find({'$or':[{'bug_title':rexExp},{'author':rexExp},{'bug_id':rexExp},{'bug_id':rexExp},{'open_date':rexExp}]})\
    .sort('open_date',pymongo.DESCENDING).skip(start).limit(num_per_page)
    conn.close()
    return res

def get_search_counts(search_params):
    #print "get_search_counts"
    conn = pymongo.MongoClient(DB_HOST,DB_PORT)
    db = conn[DB_NAME]
    coll = db[COLLECTION_NAME]
    rexExp = regex_search_params(search_params)
    #db.customer.find({'name':rexExp })
    #print search_params
    res =  coll.find({'$or':[{'bug_title':rexExp},{'author':rexExp},{'bug_id':rexExp},{'bug_id':rexExp},{'open_date':rexExp}]})
    conn.close()
    #print res[0]
    return res.count()

def get_all_counts():
    return get_search_counts('')

def regex_search_params(search_params):
    #进一步完善
    rexExp = re.compile('.*'+search_params+'.*', re.IGNORECASE)
    return rexExp