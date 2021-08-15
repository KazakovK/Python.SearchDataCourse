# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def process_prise(value):
    try:
        value = int(value)
        return value
    except:
        return value


def specifications_values(value):
    value = value.replace('\n', '').replace(' ', '')
    return value


class LmparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    prise = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(process_prise))
    specifications = scrapy.Field()
    specifications_values = scrapy.Field(input_processor=MapCompose(specifications_values))
    parameter = scrapy.Field()
    _id = scrapy.Field()