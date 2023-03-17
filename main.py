import psycopg2
from pymongo import MongoClient
import numpy as np

#Met behulp van psycopg2 kan Python verbinden met pgAdmin 4.
con = psycopg2.connect(
    host='localhost',
    database='webshop_db',
    user='postgres',
    password='1824')

con.autocommit = True
cur = con.cursor()

client = MongoClient('mongodb://localhost:27017')
db = client.get_database('huwebshop')

doc = client.huwebshop.products.find_one()

# (Mijn database heet 'huwebshop' en mijn collectie met producten heet 'product')
producten = [product for product in client.huwebshop.product.find()]


def product_to_db(producten):
    for product in producten:
        product_id = product['_id']
        naam = product['category']['category_1']
        prijs = product['price']['selling_price']
        query = ('INSERT INTO product (product_id, product_name, selling_price) VALUES(%s,%s,%s)')
        insertion_data = (product_id, naam, prijs)
        cur.execute(query, insertion_data)


def gemiddelde_prijs(producten):
    lst = []
    for product in producten:
        if 'price' in product.keys():
            lst.append(product['price']['selling_price'])
    gem = np.mean(lst)
    return gem

print(gemiddelde_prijs(producten))

def standard_deviation():
    lst = []
    deviations = []
    for product in producten:
        if 'price' in product.keys():
            lst.append(product['price']['selling_price'])
    avg = np.mean(lst)
    dev_up = max(lst) - avg
    dev_down = avg - min(lst)
    deviations.append(dev_up)
    deviations.append(dev_down)
    return max(deviations)

