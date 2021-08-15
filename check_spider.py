from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['books']
labirint = db.labirint

labirint_dic = labirint.find({})

i = 0
for item in labirint_dic:
    i += 1
    pprint(item)