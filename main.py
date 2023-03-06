import pymongo
from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://damianplomp:Np2NrQqUrUM8PyBz@cluster0.wmvdte3.mongodb.net/?retryWrites=true&w=majority")
db = client['SP-Python']

collection = db['webshop-data']


# First product in database
first_item_name = collection.find()[0]['category']['category_1']
first_item_price = collection.find()[0]['price']['selling_price']
print(f'Het eerste product uit de database is een {first_item_name}, de prijs hiervan is {first_item_price} euro')



# First product that starts with letter 'R'
res = []
for row in collection.find():
    product = row['category']['category_1']
    if product[0] == 'R':
        print(product)
        res.append(product)
if len(res) == 0:
    print('There were no items found that start with a R.')

# Average price of all products
prices = []
for row in collection.find():
    prices.append(row['price']['selling_price'])
print(f'The average price of all the products is {(sum(prices)) // (len(prices))}')
