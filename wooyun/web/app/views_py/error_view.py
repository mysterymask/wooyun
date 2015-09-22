#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from app import app 
from flask import render_template
from flask import request


@app.errorhandler(400)
def bad_request(error):
    return 'HTTP 400 Bad Request', 400
