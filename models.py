# Modelling..

import peewee
from peewee import *
from datetime import date

db = peewee.SqliteDatabase("my_database.db")

# Models go here..

class User(peewee.Model):
    name = peewee.CharField()
    address_data = peewee.CharField()
    billing_information = peewee.CharField()

    class Meta:
        my_database = db

class Product(peewee.Model):
    name = peewee.CharField()
    description = peewee.CharField()
    price_per_unit = peewee.IntegerField()
    quantity = peewee.IntegerField() 

    class Meta:
        my_database = db
       
class Price(peewee.Model):
    price = peewee.IntegerField() 

    class Meta:
        my_database = db

class Transaction(peewee.Model): 
    trans_id = peewee.AutoField()
    seller = peewee.ForeignKeyField()
    buyer = peewee.ForeignKeyField()
    product = peewee.ForeignKeyField()
    quantity = peewee.IntegerField()
    date = peewee.DateField(default=date.today())
    product = peewee.CharField(Product)
    prod_title = peewee.CharField()
    buyer_name = peewee.CharField()
    seller_name = peewee.CharField()

    class Meta:
        my_database = db

class Tag(peewee.Model):
    name = CharField()
    products = ManyToManyField(Product)

    class Meta:
        my_database = db

ProductTag = Tag.products.get_through_model()       

class Purchase(peewee.Model):
    transaction = peewee.IntegerField() 
    product = peewee.ForeignKeyField(Product)
    quantity = peewee.IntegerField()
    price = peewee.ForeignKeyField(Price)
    user = peewee.ForeignKeyField(User)
    date = peewee.DateField(default=date.today())
    time = peewee.TimeField()
    
    class Meta:
        my_database = db   

def create_tables():
 with db:
      db.create_tables([User, Product, Price, Transaction, Tag, Purchase])  