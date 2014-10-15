import os
import time
import logging

import bottle
from bottle import request
import json
from urllib import urlopen,quote
import CategoryWrapper as cw
#import SolrWrapper as sw
#import WhooshWrapper as sw
#import PiWrapper as sw
import PiWhooshCombinedWrapper as sw

app = bottle.Bottle()

@app.route('/api/status')
def status():
    return {'status': 'online', 'servertime': time.time()}


@app.route('/api/echo/<text>')
def echo(text):
    return text

@app.route('/api/search2')
def search2():
    solr_params = dict((k,request.query[k]) for k in request.query.keys())
    query = request.query.get('q',None)
    if(query!=None):
        cats = cw.lookup(query)
        cat_filter = '*'
        if len(cats)>0:
            cat_filter = "\"%s\""%'\" OR \"'.join(cats)
        solr_params.update({'fq':'raw_catpred:(%s) AND store:\"24\"'%(cat_filter)})
    return sw.search(solr_params)

@app.route('/api/search')
def search():
    solr_params = dict((k,request.query[k]) for k in request.query.keys())
    query = request.query.get('q',None)
    #if(query!=None):
    #    cats = cw.lookup(query)
    #    cat_filter = '*'
    #    if len(cats)>0:
    #        cat_filter = "\"%s\""%'\" OR \"'.join(cats)
    #    solr_params.update({'fq':'raw_catpred:(%s) AND store:\"24\"'%(cat_filter)})
    return sw.search(solr_params)

@app.route('/api/fuzzysearch')
def fuzzysearch():
    solr_params = dict((k,request.query[k]) for k in request.query.keys())
    query = request.query.get('q',None)
    if(query!=None):
    #    cats = cw.lookup(query)
    #    cat_filter = '*'
    #    if len(cats)>0:
    #        cat_filter = "\"%s\""%'\" OR \"'.join(cats)
    #    solr_params.update({'fq':'raw_catpred:(%s) AND store:\"24\"'%(cat_filter)})
        solr_params.update({'q':' '.join([tok+'~' for tok in query.split()])})
    return sw.search(solr_params)

@app.route('/api/facetsearch')
def facetsearch():
    solr_params = dict((k,request.query[k]) for k in request.query.keys())
    query = request.query.get('q',None)
    if(query!=None):
        cats = cw.lookup(query)
	print "cats:%s"%str(cats)
        cat_filter = '*'
        if len(cats)>0:
            cat_filter = "\"%s\""%'\" OR \"'.join(cats)
            cat_filter = ("(%s)" if len(cats)>1 else "%s")%cat_filter
            solr_params.update({'fq':'catpred:%s AND store:\"24\"'%(cat_filter)})
	print str(solr_params)
    return sw.search(solr_params)

@app.route('/api/fuzzyfacetsearch')
def fuzzyfacetsearch():
    solr_params = dict((k,request.query[k]) for k in request.query.keys())
    query = request.query.get('q',None)
    if(query!=None):
        cats = cw.lookup(query)
	print "cats:%s"%str(cats)
        cat_filter = '*'
        if len(cats)>0:
            cat_filter = "\"%s\""%'\" OR \"'.join(cats)
            cat_filter = ("(%s)" if len(cats)>1 else "%s")%cat_filter
            solr_params.update({'fq':'catpred:%s AND store:\"24\"'%(cat_filter)})
        solr_params.update({'q':' '.join([tok+'~' for tok in query.split()])})
    return sw.search(solr_params)
