# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LmparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['goodsLM']

    def process_item(self, item, spider):
        dict_parameter = dict(zip(item['specifications'], item['specifications_values']))
        item['parameter'] = dict_parameter
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        print()
        return item

class LmPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
