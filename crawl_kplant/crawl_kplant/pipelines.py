# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from scrapy.exceptions import DropItem


def cleaner(text):
    if text is None:
        return text
    clean = re.compile('<[^>]*>')
    text = clean.sub('', text).replace(' ', '').replace('\n', '').replace('\r', '')
    return text


class CrawlKplantPipeline:
    def process_item(self, item, spider):
        item['cName'] = cleaner(item['cName'])
        # 去除第1行有時會出現的「更多ＸＸＸ」
        item['cName'] = re.sub('\u00a0+.*', '', item['cName'])
        if item['eName'] is not None:
            item['eName'] = re.sub('<[^>]*>', '', item['eName']).replace('\n', '').replace('\r', '')
            item['eName'] = re.sub(' +', ' ', item['eName'])
        if item['sName'] is not None:
            item['sName'] = re.sub('<[^>]*>', '', item['sName']).replace('\n', '').replace('\r', '')
            item['sName'] = re.sub(' +', ' ', item['sName'])
        item['fName'] = cleaner(item['fName'])
        item['aName'] = cleaner(item['aName'])
        item['distribution'] = cleaner(item['distribution'])
        item['stem'] = cleaner(item['stem'])
        item['leaf'] = cleaner(item['leaf'])
        item['flower'] = cleaner(item['flower'])
        item['fruit'] = cleaner(item['fruit'])
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
