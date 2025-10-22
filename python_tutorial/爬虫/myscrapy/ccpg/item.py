# /usr/bin/env python3
# -*- coding:utf-8 -*-
import scrapy

class MyItem(scrapy.Item):
    name = scrapy.Field()           # 项目名称
    amount = scrapy.Field()         # 中标金额
    fromCompany = scrapy.Field()    # 采购单位
    toCompany = scrapy.Field()      # 中标单位
    url = scrapy.Field()            # url