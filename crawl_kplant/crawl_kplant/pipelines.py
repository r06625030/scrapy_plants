# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from scrapy.exceptions import DropItem
import sqlite3


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


class SQLitePipeline(object):
    # 打開database
    def open_spider(self, spider):
        db_name = spider.settings.get('SQLITE_DB_NAME')
        self.db_conn = sqlite3.connect(db_name)
        self.db_cur = self.db_conn.cursor()

    # 關閉database
    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def insert_db(self, item):
        self.db_cur.execute('SELECT cName FROM plants WHERE cName = (?)', (item['cName'],))
        result = self.db_cur.fetchone()
        if result:
            raise DropItem('Item already in database: %s' % item)
        else:
            values = (
                item['url'],
                item['fName'],
                item['cName'],
                item['eName'],
                item['sName'],
                item['gName'],
                item['aName'],
                item['stem'],
                item['leaf'],
                item['flower'],
                item['fruit'],
            )
            sql = 'INSERT INTO plants VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            self.db_cur.execute(sql, values)

    def process_item(self, item, spider):
        self.insert_db(item)
        return item
