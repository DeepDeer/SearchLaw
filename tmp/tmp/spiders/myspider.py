# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from tmp.items import tmpItem
from scrapy.spiders import BaseSpider
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#from scrapy_redis.spiders import RedisSpider


class MySpider(BaseSpider):
    name = 'myspider'
    allowed_domains = ['court.gov.cn']
    start_urls=["http://www.court.gov.cn/cpwsw/mshz/index_807.htm"]

    def parse(self, response):
    	wenshus = Selector(response).xpath('//div[@class="bottom_right_con_five_list"]/ul')
    	for wenshu in wenshus:
    		ws_href = wenshu.xpath('li/div/div[2]/a/@href').extract()[0]
    		ws_url = "http://www.court.gov.cn/cpwsw/"+ws_href[3:]
    		
    		yield Request(ws_url,callback=self.parse_items)

        myurl = str(response.url)
        info = myurl.split('/')
        mytpye = info[4]
        info_page = info[5].split('.')
        page = int(info_page[0][6:])
        if mytpye=="mshz" and page<10535:
        	nurl="http://www.court.gov.cn/cpwsw/mshz/index_"+str(page+1)+".htm"
        	yield self.make_requests_from_url(nurl)
        elif mytpye=="xshz" and page<10049:
        	nurl="http://www.court.gov.cn/cpwsw/xshz/index_"+str(page+1)+".htm"
        	yield self.make_requests_from_url(nurl)
        elif mytpye=="xzhz" and page<2861:
        	nurl="http://www.court.gov.cn/cpwsw/xzhz/index_"+str(page+1)+".htm"
        	yield self.make_requests_from_url(nurl)
        elif mytpye=="zscqhz" and page<1391:
        	nurl="http://www.court.gov.cn/cpwsw/zscqhz/index_"+str(page+1)+".htm"
        	yield self.make_requests_from_url(nurl)
        elif mytpye=="pchz" and page<24:
        	nurl="http://www.court.gov.cn/cpwsw/pchz/index_"+str(page+1)+".htm"
        	yield self.make_requests_from_url(nurl)
        elif mytpye=="zxhz" and page<2124:
        	nurl="http://www.court.gov.cn/cpwsw/zxhz/index_"+str(page+1)+".htm"
        	yield self.make_requests_from_url(nurl)

    def parse_items(self, response):
        sel = Selector(response)
        article_url = str(response.url)
        item = tmpItem()
        dstore={'bj':'北京','tj':'天津','heb':'河北','sx':'山西','nmg':'内蒙古','ln':'辽宁','jl':'吉林','hlj':'黑龙江','sh':'上海',
                'jiangsu':'江苏','zj':'浙江','ah':'安徽','fj':'福建','jx':'江西','sd':'山东','hen':'河南','hub':'湖北','hun':'湖南',
                'gd':'广东','gx':'广西','hain':'海南','cq':'重庆','sc':'四川','gz':'贵州','yn':'云南','xz':'西藏','shanxi':'陕西',
                'gs':'甘肃','qh':'青海','nx':'宁夏','xj':'新疆','bt':'兵团','zgrmfy':'最高人民法院'}
        item['link'] = article_url.encode('utf-8')
        sf0= item['link'].split('/')
        item['dq']= dstore[sf0[4]]
        item['mc'] = sel.xpath('//div[@id="wsTitle"]/text()').extract()[0]
        item['gbrq'] = sel.xpath('//div[@id="wsTime"]/span/text()').extract()[0]
        item['lx'] = sel.xpath('//div[@id="nav"]/a[last()]/text()').extract()[0]
        
        myID = sel.xpath('//div[@id="DocArea"]/div[3]/text()')
        if myID: # 应对大部分网页的排版
        	item['ID'] = myID.extract()[0]
        	item['fy'] = sel.xpath('//div[@id="DocArea"]/div[1]/text()').extract()[0]
        	mynr= sel.xpath('//div[@id="DocArea"]/div[position()>3]/text()').extract()
        	fullnr = ''
        	for h in mynr:
        		fullnr += h
        	item['nr'] = fullnr
        else:  # 比较不正常的网页排版
        	page_htm0 = sel.xpath('//div[@id="DocArea"]/div[1]/@class')
        	if page_htm0:
        		#item['ID'] = sel.xpath('//div[@id="DocArea"]/div/span/font/p[1]/span/text()').extract()[0]
        		#item['fy'] = sel.xpath('//div[@id="DocArea"]/div/p[3]/span/font/text()').extract()[0]
        		nrs = sel.xpath('//div[@id="DocArea"]/div/span/font/p[position()>1]')
        		fullnr = ''
        		for n in nrs:
        			mynr = n.xpath('span/text()').extract()
        			for h in mynr:
        				fullnr += h
        		item['nr'] = fullnr
        	else:    #比如http://www.court.gov.cn/zgcpwsw/hain/xz/201311/t20131125_175221.htm的不正常排版
        		page_htm1 = sel.xpath('//div[@id="DocArea"]/p[1]/@align')
        		if page_htm1:
        			item['ID'] = sel.xpath('//div[@id="DocArea"]/font/p[1]/text()').extract()[0]
        			item['fy'] = sel.xpath('//div[@id="DocArea"]/p[1]/font/font/text()').extract()[0]
        			mynr = sel.xpath('//div[@id="DocArea"]/font/p[2]/text()').extract()
        			fullnr = ''
        			for h in mynr:
        				fullnr += h
        			item['nr'] = fullnr        			
        		else:  # 
        			item['ID'] = sel.xpath('//div[@id="DocArea"]/p[3]/text()').extract()[0]
        			item['fy'] = sel.xpath('//div[@id="DocArea"]/p[1]/text()').extract()[0]
        			mynr= sel.xpath('//div[@id="DocArea"]/p[position()>3]/text()').extract()
        			fullnr = ''
        			for h in mynr:
        				fullnr += h
        			item['nr'] = fullnr
        			
        return item
        
