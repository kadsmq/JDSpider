# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JdItem(scrapy.Item):
    # define the fields for your item here like:
    spid = scrapy.Field()
    url_x = scrapy.Field()
    name = scrapy.Field()
    xiangqing = scrapy.Field()
    jiage = scrapy.Field()
    zhongliang = scrapy.Field()