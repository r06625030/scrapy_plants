# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlKplantItem(scrapy.Item):
    # 中名、英名、學名、科名、別名、原產地、分布、用途、莖、葉、花、果實、特徵、圖片（網址）
    cName = scrapy.Field()
    eName = scrapy.Field()
    sName = scrapy.Field()
    fName = scrapy.Field()
    aName = scrapy.Field()
    distribution = scrapy.Field()
    stem = scrapy.Field()
    leaf = scrapy.Field()
    flower = scrapy.Field()
    fruit = scrapy.Field()
    url = scrapy.Field()

