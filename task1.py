import requests
import json

user = 'KazakovK'
url = f'https://api.github.com/users/{user}/repos'
response = requests.get(url)
repos = response.json()

with open('task1.json', 'w') as outfile:
    json.dump(repos, outfile)

print(f"Репозитории пользователя: ")
for item in repos:
    print(item['name'])
