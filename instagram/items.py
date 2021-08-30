# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def process_int(value):
    try:
        value = int(value)
        return value
    except:
        return value


class InstagramItem(scrapy.Item):
    user_id = scrapy.Field(input_processor=MapCompose(process_int))
    user_id_follows = scrapy.Field(input_processor=MapCompose(process_int))
    username_follows = scrapy.Field()
    full_name_follows = scrapy.Field()
    picture_follows = scrapy.Field()
    _id = scrapy.Field()
