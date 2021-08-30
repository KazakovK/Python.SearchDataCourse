# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class InstagramPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['instfollows']

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

class InstagramPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['picture_follows']:
            try:
                yield scrapy.Request(item['picture_follows'])
            except Exception as e:
                print(e)
