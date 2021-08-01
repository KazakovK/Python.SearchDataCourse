from bs4 import BeautifulSoup as bs
import requests
import json
from pprint import pprint
import pandas as pd

user_word = input('Введите название должности: ')

url = 'https://hh.ru'

params = {'clusters': 'true',
          'text': user_word}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 YaBrowser/21.6.1.274 Yowser/2.5 Safari/537.36'}

response = requests.get(url + '/search/vacancy', params=params, headers=headers)
response.encoding = 'utf8'

soup = bs(response.text, 'html.parser')

pages_list = soup.find_all('a', attrs={'data-qa': 'pager-page'})
vacancy_dict = []

for pages in pages_list:
    page_number = pages.find('span').getText()

    params = {'clusters': 'true',
              'text': user_word,
              'page': page_number}

    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    response.encoding = 'utf8'

    soup = bs(response.text, 'html.parser')

    vacancy_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})

    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_name = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})
        vacancy_money = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
        if vacancy_name:
            vacancy_url = vacancy_name.get('href')
            vacancy_name = vacancy_name.getText()
            if vacancy_money:
                vacancy_money = vacancy_money.getText()
                vacancy_money = vacancy_money.replace('\u202f', '')
                vacancy_money = vacancy_money.split()
                vacancy_currency = vacancy_money[-1]
                if vacancy_money[0] == 'до':
                    vacancy_money_max = vacancy_money[1]
                    vacancy_money_min = None
                elif vacancy_money[0] == 'от':
                    vacancy_money_min = vacancy_money[1]
                    vacancy_money_max = None
                else:
                    vacancy_money_min = vacancy_money[0]
                    vacancy_money_max = vacancy_money[2]
            else:
                vacancy_money_min = None
                vacancy_money_max = None
                vacancy_currency = None

            vacancy_data['name'] = vacancy_name
            vacancy_data['url'] = vacancy_url
            vacancy_data['currency'] = vacancy_currency
            vacancy_data['max'] = vacancy_money_max
            vacancy_data['min'] = vacancy_money_min

            vacancy_dict.append(vacancy_data)

output = pd.DataFrame()
output = output.append(vacancy_dict, ignore_index=True)

output.to_excel('./vacancy.xlsx')
