import json
from pymongo import MongoClient

client = MongoClient('mongodb://root:rootpassword@localhost:27017')
db = client['meal_mate_db']
collection_currency = db['stored meals']

with open('teststoredmeals.json', encoding='utf-8') as f:
    file_data = json.load(f)

collection_currency.insert_many(file_data)

client.close()