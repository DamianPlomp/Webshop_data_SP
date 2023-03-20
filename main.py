import psycopg2
from pymongo import MongoClient

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
