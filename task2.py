import requests
from pprint import pprint
import json

url = 'https://api.vk.com/method/friends.get'
my_params = {'v': '5.52',
             'access_token': 'dde41440e999af0312ca23fafbab2921601da353476512ee4204bd3e42b8a30c05c3f791c47a5c05987d4',
             'fields': 'city',
             'user_id': '38582416'}
my_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 YaBrowser/21.6.1.274 Yowser/2.5 Safari/537.36'}
response = requests.get(url, params=my_params, headers=my_headers)

repos = response.json()
with open('task2.txt', 'w') as outfile:
    json.dump(repos, outfile)
pprint(repos)
