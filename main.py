# Querying..

from models import *
from fuzzywuzzy import fuzz

__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

def search(term):
    query = (Product
             .select()
             .where(
                 (Product.name.contains(term)) | 
                 (Product.description.contains(term))
             ))
    return list(query)

def list_user_products(user_id):
    query = Product.select().where(Product.user == user_id)
    return list(query)

def list_products_per_tag(tag_id):
    tag = Tag.get_by_id(tag_id)
    return list(tag.products)

def add_product_to_catalog(product):
    new_product = Product.create(**product)
    return new_product

def update_stock(product_id, new_quantity):
    product = Product.get_by_id(product_id)
    product.quantity = new_quantity
    product.save()
    return product

def purchase_product(product_id, quantity):
    product = Product.get_by_id(product_id)
    if product.quantity >= quantity:
        product.quantity -= quantity
        product.save()
        return True
    else:
        return False

def remove_product(product_id):
    product = Product.get_by_id(product_id)
    product.delete_instance()
    return True

if __name__ == "__main__":
    create_tables()
    populate_test_database()
    user, created = User.get_or_create(name="John Doe", email="john@example.com", defaults={"address_data": "123 Test St", "billing_information": "Visa 1234"})
    tag1, created1 = Tag.get_or_create(name="Clothing")
    tag2, created2 = Tag.get_or_create(name="Winter Wear")

    product_data = {
        "name": "Sweater",
        "description": "A warm sweater for winter",
        "price_per_unit": 29.99,
        "quantity": 100,
        "user": user
    }

    sweater = add_product_to_catalog(product_data)
    sweater.tags.add([tag1, tag2])

    results = search("sweater")
    print("Search results:")
    for product in results:
        print(f"Product ID: {product.id}, Name: {product.name}, Description: {product.description}, Price: {product.price_per_unit}, Quantity: {product.quantity}")

    user_products = list_user_products(user.id)
    print("\nUser products:")
    for product in user_products:
        print(f"Product ID: {product.id}, Name: {product.name}, Description: {product.description}, Price: {product.price_per_unit}, Quantity: {product.quantity}")

    tag_products = list_products_per_tag(tag1.id)
    print("\nProducts per tag 'Clothing':")
    for product in tag_products:
        print(f"Product ID: {product.id}, Name: {product.name}, Description: {product.description}, Price: {product.price_per_unit}, Quantity: {product.quantity}")

    update_stock(sweater.id, 50)
    purchase_product(sweater.id, 2)
    remove_product(sweater.id)