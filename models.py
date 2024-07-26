# Modelling.. 
# Incl. populate_test_database

import peewee
from peewee import *
from datetime import date, datetime

# Definieert database connectie = my_database.db
db = SqliteDatabase("my_database.db")

# Models
class User(Model):
    name = CharField()
    email = CharField(unique=True)
    address_data = CharField()
    billing_information = CharField()

    class Meta:
        database = db

class Product(Model):
    name = CharField()
    description = TextField()
    price_per_unit = DecimalField()
    quantity = IntegerField()
    user = ForeignKeyField(User, backref='products')

    class Meta:
        database = db

class Tag(Model):
    name = CharField(unique=True)
    products = ManyToManyField(Product, backref='tags')

    class Meta:
        database = db

ProductTag = Tag.products.get_through_model()

class Transaction(Model):
    seller = ForeignKeyField(User, backref='sales')
    buyer = ForeignKeyField(User, backref='purchases')
    product = ForeignKeyField(Product, backref='transactions')
    quantity = IntegerField()
    date = DateField(default=date.today())

    class Meta:
        database = db

class Price(Model):
    price = DecimalField()

    class Meta:
        database = db

class Purchase(Model):
    transaction = ForeignKeyField(Transaction, backref='purchases')
    product = ForeignKeyField(Product, backref='purchases')
    quantity = IntegerField()
    price = ForeignKeyField(Price, backref='purchases')
    user = ForeignKeyField(User, backref='purchases')
    date = DateField(default=date.today())
    time = TimeField(default=datetime.now().time())

    class Meta:
        database = db

def create_tables():
    with db:
        db.drop_tables([User, Product, Tag, ProductTag, Transaction, Price, Purchase])
        db.create_tables([User, Product, Tag, ProductTag, Transaction, Price, Purchase])

def populate_test_database():
    # Populate database met test data
    users = [
        {"name": "Ray", "email": "ray@example.com", "address_data": "123 Elm Street", "billing_information": "Visa 1234"},
        {"name": "Alice", "email": "alice@example.com", "address_data": "456 Oak Avenue", "billing_information": "MasterCard 5678"},
        {"name": "Bob", "email": "bob@example.com", "address_data": "789 Pine Road", "billing_information": "Amex 9012"},
        {"name": "Emma", "email": "emma@example.com", "address_data": "101 Maple Lane", "billing_information": "Discover 3456"}
    ]
    
    user_objects = []
    for user in users:
        user_obj, created = User.get_or_create(email=user['email'], defaults=user)
        user_objects.append(user_obj)

    products = [
        {"name": "Sweater", "description": "Warm and cozy sweater for cold weather", "price_per_unit": 29.99, "quantity": 100, "user": user_objects[0]},
        {"name": "T-Shirt", "description": "Casual and comfortable cotton t-shirt", "price_per_unit": 14.99, "quantity": 200, "user": user_objects[1]},
        {"name": "Jeans", "description": "Classic denim jeans for everyday wear", "price_per_unit": 39.99, "quantity": 150, "user": user_objects[2]},
        {"name": "Shoes", "description": "Stylish and durable shoes for any occasion", "price_per_unit": 49.99, "quantity": 75, "user": user_objects[3]},
        {"name": "Hat", "description": "Trendy and versatile hat to complete your look", "price_per_unit": 9.99, "quantity": 50, "user": user_objects[0]}
    ]
    product_objects = [Product.create(**product) for product in products]

    prices = [Price.create(price=p['price_per_unit']) for p in products]

    tags = ["Clothing", "Winter Wear", "Summer Wear", "Footwear", "Accessories"]
    tag_objects = []
    for tag in tags:
        tag_obj, created = Tag.get_or_create(name=tag)
        tag_objects.append(tag_obj)

    tag_objects[0].products.add(product_objects[:3])
    tag_objects[1].products.add(product_objects[0])
    tag_objects[2].products.add(product_objects[1])
    tag_objects[3].products.add(product_objects[3])
    tag_objects[4].products.add(product_objects[4])

    transactions = [
        {"seller": user_objects[0], "buyer": user_objects[1], "product": product_objects[0], "quantity": 2},
        {"seller": user_objects[1], "buyer": user_objects[2], "product": product_objects[1], "quantity": 3},
        {"seller": user_objects[2], "buyer": user_objects[3], "product": product_objects[2], "quantity": 1},
        {"seller": user_objects[3], "buyer": user_objects[0], "product": product_objects[3], "quantity": 1}
    ]
    transaction_objects = [Transaction.create(**transaction) for transaction in transactions]

    purchases = [
        {"transaction": transaction_objects[0], "product": product_objects[0], "quantity": 2, "price": prices[0], "user": user_objects[1]},
        {"transaction": transaction_objects[1], "product": product_objects[1], "quantity": 3, "price": prices[1], "user": user_objects[2]},
        {"transaction": transaction_objects[2], "product": product_objects[2], "quantity": 1, "price": prices[2], "user": user_objects[3]},
        {"transaction": transaction_objects[3], "product": product_objects[3], "quantity": 1, "price": prices[3], "user": user_objects[0]}
    ]
    [Purchase.create(**purchase) for purchase in purchases]

if __name__ == "__main__":
    create_tables()
    populate_test_database()
    print("Database populated with test data.")