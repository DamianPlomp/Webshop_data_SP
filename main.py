import psycopg2
from pymongo import MongoClient
import numpy as np

# connectie met postgreSQL
con = psycopg2.connect(
    host='localhost',
    database='webshop_db',
    user='postgres',
    password='Innerlijke_kracht12&'
)

con.autocommit = True
cur = con.cursor()

# connectie met mongoDB
client = MongoClient('mongodb://localhost:27017')
db = client.get_database('huwebshop')

# haalt lijst van alle producten op uit mongoDB
product_counts = [product for product in client.huwebshop.products.find()]


# schrijft product info naar relationele database
def product_to_db(products):
    """
    :param products: list
    :return:
    """
    for product in products:
        if '_id' in product and 'name' in product and 'price' in product and 'selling_price' in product['price']:
            product_id = product['_id']
            naam = product["name"]
            prijs = product["price"]["selling_price"]/100
            query = ('INSERT INTO product (product_id, product_name, selling_price) VALUES(%s,%s,%s)')
            insertion_data = (product_id, naam, prijs)

            try:
                cur.execute(query, insertion_data)
            except psycopg2.errors.UniqueViolation:
                # If inserting this row would result in a duplicate key error, skip it
                print(f"Skipping duplicate row with product_id={product_id}")
        else:
            print(f"Skipping product {product['_id']} due to missing fields")


product_to_db(product_counts)


def avg_price(products):
    """
    :param products: list
    :return: float
    """
    total = 0
    count = 0
    for product in products:
        if 'price' in product and 'selling_price' in product['price']:
            total += product['price']['selling_price']
            count += 1

    if count == 0:
        print("No prices found")
        return None

    gem = round(total / (count * 100), 2)

    return gem


print(avg_price(product_counts))


def deviation():
    """
    geeft de deviatie van de meest afwijkende prijs
    :return: max(deviations): int
    """
    db = client['huwebshop']
    collection = db['products']

    prices = []
    for product in collection.find():
        if 'price' in product and 'selling_price' in product['price']:
            prices.append(product['price']['selling_price'])

    if prices:
        max_price = max(prices)
        min_price = min(prices)
        biggest_deviation = max_price - min_price
        return biggest_deviation
    else:
        print("No prices found")


print(deviation())
