import pymongo
import psycopg2
from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://damianplomp:1234@data-webshop-sp.bsobel2.mongodb.net/test")
db = client['huwebshop']

collection = db['product']

connection = psycopg2.connect(host='postgres', database='webshop_db', user='postgres', password='1824')

cur = connection.cursor()

