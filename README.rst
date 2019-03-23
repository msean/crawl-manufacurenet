该爬虫爬取中国制造网相关数据 

1 运行环境:

  ubuntu 14.04 
  
  python 2.7.6 
  
  scrapy 1.0.3 
  
  redis

spider 目录：
    主要负责爬虫页面的解析，requests请求发现，去重，IP代理

scrapy_redis 目录：
    通过redis构建分布式，将所有发现的请求放在redis库中，然后所有采集设备从中调度分配请求连接 ，可以参考scrapy-redis源码：
    https://github.com/darkrho/scrapy-redis.git

statscol目录： 
    通过graphite进行爬虫监控，可以查看爬虫采集数量以及请求状态，graphite必须装在linux环境中

middlewares目录：
    设置浏览器user-agent和代理proxy
