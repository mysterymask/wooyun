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
    cous = get_all_counts("wooyun_bug")
    return render_template("index.html",
    	counts = cous)