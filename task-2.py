from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['news_database']
news_db = db.news

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 YaBrowser/21.6.1.274 Yowser/2.5 Safari/537.36'}
url = ('https://lenta.ru/', 'https://yandex.ru/news')
response = requests.get(url[0], headers=headers)

dom = html.fromstring(response.text)

news = dom.xpath("//div[@class='span4']/div[@class='first-item'] | //div[@class='span4']/div[@class='item']")

for new in news:
    day_news = {}
    name_news = new.xpath(".//a[1]/text()")
    url_news = new.xpath(".//a[1]/@href")
    time_news = new.xpath(".//a[1]/time/text()")
    url_news = "https://lenta.ru/" + url_news[0]
    name_news = name_news[0].replace('\xa0', ' ')
    time_news = time_news[0]
    day_news['name'] = name_news
    day_news['url'] = url_news
    day_news['time'] = time_news
    day_news['cource'] = "lenta.ru"

    news_db.update_one({'url': day_news['url']},
                       {'$set': day_news},
                       upsert=True)

response = requests.get(url[1], headers=headers)
dom = html.fromstring(response.text)

news = dom.xpath(
    "//div[contains(@class, 'mg-top-rubric-flexible-stories')][1]/div[contains(@class, 'mg-grid__col_xs_4')] |"
    "//div[contains(@class, 'mg-top-rubric-flexible-stories')][1]/div[contains(@class, 'mg-grid__col_xs_8')]/div[contains(@class, 'mg-grid__row_gap_8')]/div[contains(@class, 'mg-grid__col_xs_6')]")

for new in news:
    day_news = {}
    name_news = new.xpath(".//h2[@class='mg-card__title']/text()")
    url_news = new.xpath(".//a[@class='mg-card__link']/@href")
    source_news = new.xpath(".//a[@class='mg-card__source-link']/text()")
    time_news = new.xpath(".//span[@class='mg-card-source__time']/text()")

    name_news = name_news[0].replace('\xa0', ' ')
    url_news = url_news[0]
    source_news = source_news[0]
    time_news = time_news[0]

    day_news['name'] = name_news
    day_news['url'] = url_news
    day_news['cource'] = source_news
    day_news['time'] = time_news

    news_db.update_one({'url': day_news['url']},
                       {'$set': day_news},
                       upsert=True)

news_dic = news_db.find({})
for new in news_dic:
    pprint(new)
