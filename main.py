import pymongo
from pymongo import MongoClient
import json

cluster = MongoClient("mongodb+srv://damianplomp:<Np2NrQqUrUM8PyBz>@cluster0.wmvdte3.mongodb.net/?retryWrites=true&w=majority")
db = cluster['SP-Python']
collection = db['test']

collection.insert_one({})

