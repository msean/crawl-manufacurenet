# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ManufacturenetItem(Item):
    # define the fields for your item here like:
    category = Field()        #所在分类
    goods = Field()           #物品名称
    MOQ = Field()             #起订量
    price = Field()           #价格
    totalSupply = Field()     #供货总量
    Orgin = Field()           #产地
    deliveryDate = Field()    #发货期
    company = Field()         #公司
    contactPerson  = Field()  #联系人
    contactNum = Field()      #联系电话
    faxNumber = Field()       #传真
    companyAdress = Field()   #公司地址
    colletTime = Field()      #采集时间
    imageUrl = Field()        #图片源网址
    pageUrl = Field()         #网页链接地址
    pack = Field()            #包装
    genre = Field()           #类型
    norms = Field()           #规格
    application = Field()     #用途
    model = Field()           #型号
    tradeMark = Field()       #商标
    productDetails = Field()  #详细介绍
    output = Field()          #产量
