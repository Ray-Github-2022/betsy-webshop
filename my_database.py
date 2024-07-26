# My database..
# Run: python main.py = Creert de database en toont de output in CLI
# Database weergeven in CLI = transactie en tag zijn gereserveerde trefwoorden in sql..
# Bij gebruik van dubbele aanhalingstekens werkt het zoals de bedoeling is:
# Run: sqlite3 my_database.db & vervolgens execute onderstaande commands..
# ."tables"                     -- Geeft een overzicht van alle tabellen in de database
# SELECT * FROM "user";         -- Toont alle records in the "user" table
# SELECT * FROM "product";      -- Toont alle records in de "product" tabel
# SELECT * FROM "transaction";  -- Toont alle records in de "transaction" tabel
# SELECT * FROM "tag";          -- Toont alle records in de "tag" tabel

import peewee
from models import *

def add_user(name, email, address_data, billing_information):
    return User.create(name=name, email=email, address_data=address_data, billing_information=billing_information)

def add_product(name, description, price, quantity, user):
    return Product.create(name=name, description=description, price_per_unit=price, quantity=quantity, user=user)

def add_transaction(seller, buyer, product, quantity):
    return Transaction.create(seller=seller, buyer=buyer, product=product, quantity=quantity)

def add_tag(name):
    return Tag.create(name=name)

def get_all_users():
    return list(User.select())

def get_all_products():
    return list(Product.select())

def get_all_transactions():
    return list(Transaction.select())

def get_all_tags():
    return list(Tag.select())