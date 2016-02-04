#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
from pyes import *
from models import Results

PAGE_SIZE=10

def dosearch(string,upage,total_hits):
    conn = ES('127.0.0.1:9200', timeout=3.5)#Connect to ES
    fq_fy = TermQuery()
    fq_fy.add('fy',string)
    
    fq_mc = TermQuery()
    fq_mc.add('mc',string)
    
    fq_nr = TermQuery()
    fq_nr.add('nr',string)
    

    bq = query.BoolQuery(should=[fq_fy,fq_mc,fq_nr])

    #add highlight to the search key word
    h=HighLighter(['<font color="yellow">'], ['</font>'], fragment_size=100)
    
    page = int(upage.encode('utf-8'))
    if page < 1:
        page = 1

    s=Search(bq,highlight=h,start=(page-1)*PAGE_SIZE,size=PAGE_SIZE,sort='gbrq')
    s.add_highlight("fy")
    s.add_highlight('mc')
    s.add_highlight('nr')
    results=conn.search(s,indices='law',doc_types='ws')
    
    #return the total hits by using a list object
    total_hits.append(results.total)
    
    #print total_hits[0]

    list=[]
    for r in results:
        if(r._meta.highlight.has_key("fy")):
            r['fy']=r._meta.highlight[u"fy"][0]
        if(r._meta.highlight.has_key('mc')):
            r['mc']=r._meta.highlight[u'mc'][0]
        if(r._meta.highlight.has_key('nr')):
            r['nr']=r._meta.highlight[u'nr'][0]

        res = Results()
        res.mc = r['mc']
        res.fy = r['fy']
        res.link = r['link']
        res.lx = r['lx']
        res.gbrq = r['gbrq']
        res.nr = r['nr'][0:250]
        res.dp = r['dq']
        list.append(res)
    return list
