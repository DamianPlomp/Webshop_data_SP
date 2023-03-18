import psycopg2
from pymongo import MongoClient
import numpy as np

#connectie met postgreSQL
con = psycopg2.connect(
    host='localhost',
    database='webshop_db',
    user='postgres',
    password='1824')

con.autocommit = True
cur = con.cursor()

#connectie met mongoDB
client = MongoClient('mongodb://localhost:27017')
db = client.get_database('huwebshop')

doc = client.huwebshop.products.find_one()

#haalt lijst van alle producten op uit mongoDB
products = [product for product in client.huwebshop.product.find()]

#schrijft product info naar relationele database
def product_to_db(products):
    """
    :param products: list
    :return:
    """
    for product in products:
        product_id = product['_id']
        naam = product['category']['category_1']
        prijs = product['price']['selling_price']
        query = ('INSERT INTO product (product_id, product_name, selling_price) VALUES(%s,%s,%s)')
        insertion_data = (product_id, naam, prijs)
        cur.execute(query, insertion_data)


def avg_price(products):
    """
    geeft de gemiddelde prijs van alle producten
    :param products: list
    :return: gem: float
    """
    lst = []
    for product in products:
        if 'price' in product.keys():
            lst.append(product['price']['selling_price'])
    gem = np.mean(lst)
    return gem


def deviation():
    """
    geeft de deviatie van de meest afwijkende prijs
    :return: max(deviations): int
    """
    lst = []
    deviations = []
    for product in products:
        if 'price' in product.keys():
            lst.append(product['price']['selling_price'])
    avg = np.mean(lst)
    dev_up = max(lst) - avg
    dev_down = avg - min(lst)
    deviations.append(dev_up)
    deviations.append(dev_down)
    return max(deviations)