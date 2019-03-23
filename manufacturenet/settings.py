# -*- coding: utf-8 -*-

# Scrapy settings for manufacturenet project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os

REDIS_URL = None
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

BOT_NAME = 'manufacturenet'

SPIDER_MODULES = ['manufacturenet.spiders']
NEWSPIDER_MODULE = 'manufacturenet.spiders'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'manufacturenet.middlewares.proxy_download_middlerware.ProxyMiddleware': 200,
    'manufacturenet.middlewares.rotate_useragent.RotateUserAgentMiddleware': 500,
}

SPIDER_MIDDLEWARES = {
    'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None,
}

DOWNLOAD_DELAY = 0.25

RECORD_RESPONSE_FILE = os.path.join(PROJECT_DIR, "record_response.log")
RECORD_CRAWLED_URL_FILE = os.path.join(PROJECT_DIR, "crawled_url.log")
SHOUDER_CRAWL_FILE = os.path.join(PROJECT_DIR, "task_url.log")

REDIRECT_ENABLED = True
ITEM_PIPELINES = {
    'manufacturenet.pipelines.ManufacturenetPipeline': 300,
    'manufacturenet.scrapy_redis.pipelines.RedisPipeline': 500,
}

GRAPHITE_HOST = '192.168.0.93'
GRAPHITE_PORT = 2003
STATS_CLASS = 'manufacturenet.statscol.graphite.RedisGraphiteStatsCollector'

SCHEDULER = "manufacturenet.scrapy_redis.scheduler.Scheduler"
QUEUE_CLASS = 'manufacturenet.scrapy_redis.queue.SpiderPriorityQueue'
SCHEDULER_PERSIST = True



