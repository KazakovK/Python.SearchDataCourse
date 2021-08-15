from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lmparser import settings
from lmparser.spiders.lm import LmSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    user_goods = input('Введите название товара: ')
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LmSpider, search=user_goods)

    process.start()
