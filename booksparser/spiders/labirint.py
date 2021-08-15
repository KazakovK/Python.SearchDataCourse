import scrapy
from scrapy.http import HtmlResponse
from booksparser.items import BooksparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/Python/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='product-title-link']/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.books_parse)

    def books_parse(self, response: HtmlResponse):
        book_url = response.url
        book_name = response.xpath("//h1/text()").extract_first()
        book_author = response.css("div.authors a::text").extract_first()
        book_price = int(response.css("div.buying-priceold-val span::text").extract_first())
        book_sale = int(response.css("div.buying-pricenew-val span::text").extract_first())
        book_rate = float(response.xpath("//div[@id='rate']/text()").extract_first())
        book_id = response.xpath("//div[@id='product-info']/@data-product-id").extract_first()
        yield BooksparserItem(url=book_url, name=book_name, author=book_author, price=book_price, sale=book_sale,
                              rate=book_rate, _id=book_id)
