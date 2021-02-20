# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import CrawlKplantItem
import re
import json


class KplantSpider(scrapy.Spider):
    name = 'kplant'
    allowed_domains = ['kplant.biodiv.tw']
    start_urls = ['http://kplant.biodiv.tw/123/植物目錄-分科索引.htm']

    def parse(self, response):
        # 提取每科連結
        '''
        links = LinkExtractor(restrict_css='td').extract_links(response)
        for link in links:
            if '科' in link.text:
                yield scrapy.Request(link.url, callback=self.plant_parse)'''
        with open('familyUrl.json', newline='') as jsonfile:
            links = json.load(jsonfile)
            for link in links:
                yield scrapy.Request(link['link'], callback=self.family_parse)

    def family_parse(self, response):
        # 取得物種名
        plant_links = LinkExtractor(restrict_css='td').extract_links(response)
        for plant_link in plant_links:
            plant = CrawlKplantItem()
            # 取得url後賦值給plant['url']再傳遞到plant_parse取得其他屬性
            plant['url'] = plant_link.url
            yield scrapy.Request(plant_link.url, meta={'key': plant}, callback=self.plant_parse)

    def plant_parse(self, response):
        plant = response.meta['key']
        plant['cName'] = response.xpath('//tr/td[1][contains(.,"‧中")]/following-sibling::td[1]').extract_first()
        plant['eName'] = response.xpath('//tr/td[1][contains(.,"‧英")]/following-sibling::td[1]').extract_first()
        plant['sName'] = response.xpath('//tr/td[1][contains(.,"‧學")]/following-sibling::td[1]').extract_first()
        # 有的頁面植物有多種學名分在不同列，因此列數可能會有不同
        sRows = response.xpath('//tr/td[1][contains(.,"‧學")]').extract_first()
        if sRows is not None:
            if 'rowspan' in sRows:
                rows = int(re.findall('rowspan="(\S*)"', sRows)[0])
                for row in range(rows - 1):
                    plant['sName'] = plant['sName'] + ' ' + response.xpath(
                        '//table[2]//tr[{}]/td'.format(4 + row)).extract_first()
        plant['fName'] = response.xpath('//tr/td[1][contains(.,"‧科")]/following-sibling::td[1]').extract_first()
        plant['aName'] = response.xpath('//tr/td[1][contains(.,"‧別")]/following-sibling::td[1]').extract_first()
        plant['distribution'] = response.xpath('//tr/td[1][contains(.,"‧分")]/following-sibling::td[1]').extract_first()
        plant['stem'] = response.xpath(
            '//tr/td[1][contains(.,"‧莖") or contains(.,"‧配子體")]/following-sibling::td[1]').extract_first()
        plant['leaf'] = response.xpath('//tr/td[1][contains(.,"‧葉")]/following-sibling::td[1]').extract_first()
        plant['flower'] = response.xpath('//tr/td[1][contains(.,"‧花")]/following-sibling::td[1]').extract_first()
        plant['fruit'] = response.xpath(
            '//tr/td[1][contains(.,"‧果") or contains(.,"‧孢子體")]/following-sibling::td[1]').extract_first()
        yield plant
