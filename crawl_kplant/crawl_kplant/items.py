# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlKplantItem(scrapy.Item):
    # 網址、科名、中名、英名、學名、屬名、別名、莖、葉、花、果實
    url = scrapy.Field()
    fName = scrapy.Field()
    cName = scrapy.Field()
    eName = scrapy.Field()
    sName = scrapy.Field()
    gName = scrapy.Field()
    aName = scrapy.Field()
    stem = scrapy.Field()
    leaf = scrapy.Field()
    flower = scrapy.Field()
    fruit = scrapy.Field()


