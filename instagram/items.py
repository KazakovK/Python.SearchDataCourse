# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramItem(scrapy.Item):
    username = scrapy.Field()
    user_id = scrapy.Field()
    picture = scrapy.Field()
    likes = scrapy.Field()
    post_data = scrapy.Field()
    _id = scrapy.Field()
