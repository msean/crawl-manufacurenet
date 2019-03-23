# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs 
import socket
from logging import log
import uuid
import os

socket.setdefaulttimeout(30)


class ManufacturenetPipeline(object):
    
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, indent=4) + "\n"
        file_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir)),'Download')
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        file_name = str(uuid.uuid5(uuid.NAMESPACE_DNS, item['pageUrl'].encode('utf8')))
        file_path = os.path.join(file_dir, file_name+".json")
        with codecs.open(file_path, 'w', encoding='utf-8') as fp:
            fp.write(line)
