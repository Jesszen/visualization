# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class WowPipeline(object):
    def process_item(self, item, spider):
        return item

class mongdo_pipeline(object):
    def __init__(self,mongo_url,mongo_coll):
        self.mongo_url=mongo_url
        self.mongo_coll=mongo_coll
    @classmethod
    def from_crawler(cls,crawler):
        return cls(mongo_url=crawler.settings.get('MONGO_URL'),
                   mongo_coll=crawler.settings.get('MONGO_COLL'))
    def open_spider(self,spider):
        self.db=pymongo.MongoClient(self.mongo_url)
        self.coll=self.db[self.mongo_coll]

    def process_item(self,item,spider):
        self.coll[item.collection].insert(dict(item))
        return item
    def close_spider(self,spider):
        self.db.close()
