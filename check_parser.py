from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['goodsLM']
lm = db.lm

lm_dic = lm.find({})

i = 0
for item in lm_dic:
    pprint(item)