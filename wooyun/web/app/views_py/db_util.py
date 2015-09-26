#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pymongo
import re
from settings import *



def search(search_params,page_index,num_per_page,collection_name):
    conn = pymongo.MongoClient(DB_HOST,DB_PORT)
    db = conn[DB_NAME]
    coll = db[collection_name]
    rexExp = regex_search_params(search_params)
    start = (page_index-1) * num_per_page
    res =  coll.find({'$or':[{'bug_title':rexExp},{'author':rexExp},{'bug_id':rexExp},{'bug_type':rexExp},{'open_date':rexExp},{'page_content':rexExp}]})\
    .sort('open_date',pymongo.DESCENDING).skip(start).limit(num_per_page)
    conn.close()
    return res

def get_search_counts(search_params,collection_name):
    conn = pymongo.MongoClient(DB_HOST,DB_PORT)
    db = conn[DB_NAME]
    coll = db[collection_name]
    rexExp = regex_search_params(search_params)
    res =  coll.find({'$or':[{'bug_title':rexExp},{'author':rexExp},{'bug_id':rexExp},{'bug_type':rexExp},{'open_date':rexExp},{'page_content':rexExp}]})
    conn.close()
    return res.count()

def get_all_counts(collection_name):
    return get_search_counts('',collection_name)

def regex_search_params(search_params):
    #进一步完善
    kws = ['.*'+ks+'.*' for ks in search_params.strip().split(' ') if ks!='']
    rexExp = re.compile('|'.join(kws), re.IGNORECASE)
    return rexExp