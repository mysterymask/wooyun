#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from app import app 
from flask import render_template
from db_util import *
@app.route('/') 
@app.route('/index')
def index():
    bug_cous = get_all_counts("wooyun_bug")
    doc_cous = get_all_counts("wooyun_doc")
    return render_template("index.html",
    	bug_counts = bug_cous,
    	doc_counts = doc_cous)