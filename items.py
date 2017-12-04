# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CheaaItem(scrapy.Item):
    # define the fields for your item here like:
    startUrl=scrapy.Field()
    LinkUrl = scrapy.Field() ##链接
    Title=scrapy.Field()  ##标题
    Time=scrapy.Field()
    InfoFrom=scrapy.Field()
    ArtcleContent=scrapy.Field()
    ProgramStarttime=scrapy.Field()
    pass
