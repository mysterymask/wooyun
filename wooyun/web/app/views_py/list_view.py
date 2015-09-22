#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from app import app 
from flask import render_template
from flask import request
from db_util import *
from settings import *
import math

@app.route('/list', methods = ['GET', 'POST']) 
def list():
    #search_param = request.form['bug_key']
    search_param = request.args.get('bug_key')
    page_ind = int(request.args.get('page',1))

    if page_ind <0 : page_ind = 1
    res_count = get_search_counts(search_param)
   
    num_per_page = NUM_PER_PAGE
    #print "res_count>>>>"+str(res_count)+">>>>"+str(num_per_page)
    pcount = int(math.ceil(res_count/(num_per_page*1.0)))
    page_infor ={'page_index':page_ind, 'records_per_page':NUM_PER_PAGE, 'page_count':pcount}

    res = []
    #print "page_ind>>>>"+str(page_ind)+">>>>"+str(pcount)	
    if pcount >0 and page_ind <= pcount:
      res = search(search_param,page_ind,num_per_page)
    return render_template("list.html",
    	search_params=search_param,
    	result_count=res_count,
    	infors = res,
    	page_infor = page_infor
    	)