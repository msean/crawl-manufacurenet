import random
from manufacturenet.scrapy_redis import connection


class ProxyMiddleware(object):

    IP_POOL_KEY = "proxy_ip:pool"

    def __init__(self, server):
        self.server = server
        cache_ip_pool = self.server.smembers(self.IP_POOL_KEY)
        self.ip_pool = [ip.split(":", 2) for ip in cache_ip_pool] if cache_ip_pool else [["localhost", "8080", "http"]]

    @classmethod
    def from_settings(cls, settings):
        server = connection.from_settings(settings)
        return cls(server)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls.from_settings(settings)

    def generate_ip(self):
        host, port, proxy_type = random.sample(self.ip_pool, 1)[0]
        return host, port, proxy_type.lower()

    def process_request(self, request, spider):
        host, port, proxy_type = self.generate_ip()
        request.meta['proxy'] = "%s://%s:%s" % (proxy_type, host, port)
