from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['goods_database']
goods_db = db.goods

goods_dic = goods_db.find( {} )

for good in goods_dic:
    pprint(good)