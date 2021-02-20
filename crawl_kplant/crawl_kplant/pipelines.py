# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from scrapy.exceptions import DropItem


class NoneElementPipeline:
    def process_item(self, item, spider):
        for element in item:
            if item[element] is None:
                item[element] = ''
        return item


class CrawlKplantPipeline:
    def cleaner(self, text):
        clean = re.compile('<[^>]*>')
        text = clean.sub('', text).replace(' ', '').replace('\n', '').replace('\r', '')
        return text

    def process_item(self, item, spider):
        item['cName'] = self.cleaner(item['cName'])
        # 去除第1行有時會出現的「更多ＸＸＸ」
        item['cName'] = re.sub('\u00a0+.*', '', item['cName'])
        item['eName'] = re.sub('<[^>]*>', '', item['eName']).replace('\n', '').replace('\r', '')
        item['eName'] = re.sub(' +', ' ', item['eName'])
        item['sName'] = re.sub('<[^>]*>', '', item['sName']).replace('\n', '').replace('\r', '')
        item['sName'] = re.sub(' +', ' ', item['sName'])
        item['gName'] = self.cleaner(item['gName'])
        item['aName'] = self.cleaner(item['aName'])
        item['stem'] = self.cleaner(item['stem'])
        item['leaf'] = self.cleaner(item['leaf'])
        item['flower'] = self.cleaner(item['flower'])
        item['fruit'] = self.cleaner(item['fruit'])
        return item


class DuplicatesTitlePipeline(object):
    def __init__(self):
        self.article = set()

    def process_item(self, item, spider):
        title = item['cName']
        if title in self.article:
            raise DropItem('duplicates title found %s', item)
        self.article.add(title)
        return (item)
