from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['instfollows']
insta = db.instagramspider


follows = insta.find({'user_id': "4299571096"})
for item in follows:
    pprint(item)

