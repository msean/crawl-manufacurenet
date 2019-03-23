# -*- coding: utf-8 -*-
import re
import time
from w3lib.html import remove_entities
from urllib.parse import urljoin

from scrapy.selector import Selector
try:  
    from scrapy.spiders import Spider  
except:  
    from scrapy.spiders import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.http import Request

from manufacturenet.items import ManufacturenetItem

extract_data_handler = lambda data_list: data_list[0].strip() if data_list else ""

compound_data  = lambda data_list: data_list[0].strip() if len(data_list) ==1 else " ".join([data.strip() for data in data_list])

clean_data = lambda data: data.strip('?').strip().strip('&nbsp;')

clean_link = lambda link_text: link_text.strip("\t\r\n '\"")

clean_url = lambda base_url, u, response_encoding: urljoin(base_url, remove_entities(clean_link(u.decode(response_encoding))))


class ManufactureNetSpider(Spider):

    name = "manufanet"
    allow_domains = ["made-in-china.com"]
    start_urls = ["http://cn.made-in-china.com/"]

    def __init__(self):
        super(ManufactureNetSpider, self).__init__()

    def parse(self,response):
        selector = Selector(response)
        base_url = get_base_url(response)
        form_urls = selector.css('div[class^="floor js"] li[class^="dir-item"] a[class="fwb"]::attr(href)').extract()

        for url in form_urls[:]:
            form_url = clean_url(base_url, url, response.encoding)
            yield Request(url=form_url, callback=self.parse_classify_form)
            
    def parse_classify_form(self, response):
        
        base_url = get_base_url(response)
        selector = Selector(response)

        follow_page_links = selector.xpath('//div[@class="pager-nav"]//a/@href').extract()
        for follow_page_link in follow_page_links[:0]:
            follow_page_url = clean_url(base_url, follow_page_link, response.encoding)
            yield Request(url=follow_page_url, callback=self.parse_classify_form)
        
        item_urls = selector.css('form[method="get"] h3 a[target="_blank"]::attr(href)').extract()
        standby_item_urls = selector.css('form[method="get"] h4 a[target="_blank"]::attr(href)').extract()
        item_urls.extend(standby_item_urls)
       
        if len(item_urls) == 0:
            exhibition_entrance_urls = selector.xpath('//div[@id="catlist"]/ul/li/a/@href').extract()
            for url in exhibition_entrance_urls[:0]:
                exhibition_entrance_url = clean_url(base_url, url, response.encoding)
                yield Request(url=exhibition_entrance_url, callback=self.parse_classify_form)
        else:
            for item in item_urls[:10]:
                item_url = clean_url(base_url, item, response.encoding)
                meta = {
                            'dont_redirect': True,
                            'handle_httpstatus_list': [302],
                            'httpcache_enabled': True,
                            'httpcache_ignore_http_codes': [302],
                            'pageUrl': item_url
                        }
                yield Request(url=item_url, meta=meta, callback=self.parse_item)
   
    def parse_item(self, response):

        selector = Selector(response)
        item = ManufacturenetItem()
        base_url = get_base_url(response)

        item['pageUrl'] = response.meta['pageUrl']

        item['goods'] = extract_data_handler(selector.css('div[class="halfImg clear"] div[class="rightCon"] h1::text').extract())
        category_fragment = selector.css('div[id="dir"] a::text').extract()
        category_fragment_handle = [clean_data(fragment) for fragment in category_fragment]
        item["category"] = ">>".join(category_fragment_handle[2:])
        item['MOQ'] = compound_data(selector.xpath('//table[@class="prices"]//tr[position()>1]//td[1]//text()').extract())       
        item['price'] = compound_data(selector.xpath('//table[@class="prices"]//tr[position()>1]//td[2]//text()').extract())
        item['totalSupply'] = extract_data_handler(selector.xpath('//table[@id="prodetails_data"]//tr[1]/td/text()').extract())
        item['Orgin'] = extract_data_handler(selector.xpath('//table[@id="prodetails_data"]//tr[2]/td/text()').extract())
        item['deliveryDate'] = extract_data_handler(selector.xpath('//table[@id="prodetails_data"]//tr[last()]/td/text()').extract())
        item['company'] = extract_data_handler(selector.xpath('//div[@class="companyName-free"]//h2[@class="only-tit"]/text()').extract())
        if item['company'] == "":
            item['company'] = extract_data_handler(selector.xpath('//div[@class="companyName"]//div[@class="only-tit"]/text()').extract())
        if item['company'] == "":
            item['company'] = extract_data_handler(selector.xpath('//div[@class="companyName"]//h2/text()').extract())

        contact_person_info = selector.xpath('//div[@class="boxCont boxText contactCard"]//li[1]//text()').extract()
        item['contactPerson'] = "".join([clean_data(info).strip(u'经理').strip(u'销售') for info in contact_person_info])

        contact_no = re.search("\d.+", extract_data_handler(selector.xpath('//div[@class="boxCont boxText contactCard"]//li[3]/text()').extract())).group()
        contact_no_standby = extract_data_handler(selector.xpath('//div[@class="boxCont boxText contactCard"]//li[@class="item"]/text()').extract())
        item['contactNum'] = "  ".join([contact_no, contact_no_standby])

        item['faxNumber'] = re.search("\d.+", extract_data_handler(selector.xpath('//div[@class="boxCont boxText contactCard"]//li[last()-1]/text()').extract())).group()

        try:
            item['companyAdress'] = extract_data_handler(selector.xpath('//div[@class="boxCont boxText contactCard"]//li[last()]/text()').extract()).split(u'：')[-1]
        except:
            item['companyAdress'] = extract_data_handler(selector.xpath('//div[@class="boxCont boxText contactCard"]//li[last()]/text()').extract())
            
        item['colletTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        item['imageUrl'] = extract_data_handler(selector.xpath('//div[@class="detailPhoto"]//a[@class="jqzoom"]/@data-url').extract())
        if item['imageUrl'] == "":
            item['imageUrl'] = extract_data_handler(selector.xpath('//div[@class="detailPhoto"]//img[@class="imgborderdetails"]/@src').extract())
        nophoto = extract_data_handler(selector.xpath('//div[@class="detailPhoto"]//img[@class="noPhoto160"]/@src').extract())
        if not item['imageUrl'] and len(nophoto) == 0:
            url_list = selector.xpath('//div[@class="main"]//div[@class="proitem"]//h3//a//@href').extract()
            for url in url_list:
                url = clean_url(base_url, url, response.encoding)
                yield Request(url=url, callback=self.parse_item)
    
        para_descriptions_rudiment = selector.xpath('//div[@class="de-table"]//div[@class="de-table-bd clear"]//td/text()').extract()
        para_descriptions = [description.strip() for description in para_descriptions_rudiment]
       
        para_dict = {
                       "application": u'用途：',
                       "genre": u'类型：',
                       "norms": u'规格：',
                       "pack": u'包装：',
                       "model": u'型号：',
                       "tradeMarkPre": u'商标：',
                       "tradeMarkStandby": u'品牌：',
                       "output": u"产量：",
        }

        self.match_para(para_dict, item, para_descriptions)
        productDetails = selector.xpath('//div[@class="de-detail"]//div[@class="de-detail-bd"]//text()').extract()

        detail_vessel = []  
        if productDetails:
            for detail in productDetails:
                detail_info = clean_data(detail)
                if detail_info:
                    detail_vessel.append(detail_info)
        item['productDetails'] = ' '.join(detail_vessel)
        yield item
        
    def get_value_index(self, value, para_descriptions):
        for index, item in enumerate(para_descriptions):
            if item == value:
                return index
             
    def match_para(self,para_dict, item, para_descriptions):
        item["tradeMark"] = ""
        for key, value in para_dict.items():
            if value in para_descriptions:
                index = self.get_value_index(value, para_descriptions)
                if key == "tradeMarkPre" or key == "tradeMarkStandby":
                    item["tradeMark"] = para_descriptions[index+1]
                else:
                    item[key] = para_descriptions[index+1] 
            else:
                if key not in ["tradeMarkPre", "tradeMarkStandby"]:
                    item[key] = ""
