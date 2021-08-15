import scrapy
from scrapy.http import HtmlResponse
from lmparser.items import LmparserItem
from scrapy.loader import ItemLoader


class LmSpider(scrapy.Spider):
    name = 'lm'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(LmSpider, self).__init__()
        self.start_urls = [f'https://samara.leroymerlin.ru/search/?q={search}']


    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='product-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=LmparserItem(), response=response)
        loader.add_xpath("name", "//h1/text()")
        loader.add_xpath("photos", '//picture[@slot="pictures"]/img/@data-origin')
        loader.add_xpath("prise", "//span[@slot='price']/text()")
        loader.add_xpath("specifications", "//dt[@class='def-list__term']/text()")
        loader.add_xpath("specifications_values", "//dd[@class='def-list__definition']/text()")
        loader.add_value("url", response.url)
        yield loader.load_item()
