from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['hh_database']
vacancy_db = db.vacancy

user_money = int(input('Введите желаемую зарплату: '))
user_word = input('Укажите валюту (руб.,KZT,USD): ')

for doc in db.vacancy.find(
        {'currency': user_word, '$or': [{'max': {'$gte': user_money}}, {'min': {'$gte': user_money}}]},
        {'name': 1, 'min': 1, 'max': 1, 'url': 1, 'currency': 1}):
    print(doc)
