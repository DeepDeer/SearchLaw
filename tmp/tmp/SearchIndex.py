#!/usr/bin/env python
#-*- coding:utf-8-*-
import os
import sys
from pyes import *
from tmp.items import tmpItem

INDEX_NAME='law'

class SearchIndex(object):

	def SearchInit(self):
		self.conn = ES('127.0.0.1:9200', timeout=3.5)#Connect to ES
		try:
			self.conn.delete_index(INDEX_NAME)
		#pass
		except:
			pass
		self.conn.indices.create_index_if_missing(INDEX_NAME)#change
        
        #Define the structure of the data format
		mapping = {u'link': {'boost': 1.0,
							'index': 'not_analyzed',
                    		'store': 'yes',
                    		'type': u'string',
                    		'term_vector' : 'with_positions_offsets'},
	               u'fy':{'boost': 1.0,
	           			  'index': 'analyzed',
	                      'store': 'yes',
	                      'type': u'string',
	                      'analyzer':'ik',
	                      'term_vector' : 'with_positions_offsets'},
	               u'mc':{'boost': 1.0,
	           		      'index': 'analyzed',
	                      'store': 'yes',
	                      'type': u'string',
	                      'analyzer':'ik',
	                      'term_vector' : 'with_positions_offsets'},
	               u'ID':{'boost': 1.0,
	           		      'index': 'not_analyzed',
	                      'store': 'yes',
	                      'type': u'string',
	                      'term_vector' : 'with_positions_offsets'},
	               u'gbrq':{'boost': 1.0,
	           		        'index': 'analyzed',
	                        'store': 'yes',
	                        'type': u'string',
	                        'analyzer':'ik',
	                        'term_vector' : 'with_positions_offsets'},
	               u'nr':{'boost': 1.0,
	           		      'index': 'analyzed',
	                      'store': 'yes',
	                      'type': u'string',
	                      'analyzer':'ik',
	                      'term_vector' : 'with_positions_offsets'},
	               u'lx':{'boost': 1.0,
	           		      'index': 'not_analyzed',
	                      'store': 'yes',
	                      'type': u'string',
	                      'term_vector' : 'with_positions_offsets'},
	               u'dq':{'boost': 1.0,
	           		      'index': 'not_analyzed',
	                      'store': 'yes',
	                      'type': u'string',
	                      'term_vector' : 'with_positions_offsets'},
		}
		self.conn.indices.put_mapping("ws", {'properties':mapping}, [INDEX_NAME])
	
	def AddIndex(self,item):
		print 'Adding Index item URL %s'% item['ID'].encode('utf-8')
		self.conn.index({'link':item['link'].encode('utf-8'), \
				'fy':item['fy'].encode('utf-8'),\
				'mc':item['mc'].encode('utf-8'),\
				'ID':item['ID'].encode('utf-8'),\
				'gbrq':item['gbrq'].encode('utf-8'),\
				'nr':item['nr'].encode('utf-8'),\
				'lx':item['lx'].encode('utf-8'),\
				'dq':item['dq'].encode('utf-8')\
			},INDEX_NAME,'ws')

	def IndexDone(self):
		self.conn.default_indices=[INDEX_NAME]#Set the default indices
		self.conn.refresh()#Refresh the ES
