from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

url = 'https://hh.ru'

params = {'clusters': 'true',
          'text': 'php'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 YaBrowser/21.6.1.274 Yowser/2.5 Safari/537.36'}

response = requests.get(url + '/search/vacancy', params=params, headers=headers)

