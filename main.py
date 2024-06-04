# Querying..

from peewee import *
from fuzzywuzzy import fuzz

__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

def search(term):
    """ Search for products based on a term. Searching for 'sweater' should yield all 
        products that have the word 'sweater' in the name or description => case-insensitive """
    products = [] 
    results = []
    for product in products:
        if term.lower() in product['name'].lower() or term.lower() in product.get('description', '').lower():
            name_ratio = fuzz.ratio(term.lower(), product['name'])
            description_ratio = fuzz.ratio(term.lower(), product['description'])

        if name_ratio >= 70 or description_ratio >= 70:
            results.append(product)

    return results

def list_user_products(user_id):
    """ View the products of a given user. """
    user_products = {} 
    if user_id in user_products:
        return user_products[user_id]
    else:
        return []

def list_products_per_tag(tag_id):
    """ View all products for a given tag. """
    tag_products = {}
    if tag_id in tag_products:
        return tag_products[tag_id]
    else:
        return []

def add_product_to_catalog(user_id, product):
    """ Add a product to a user. """
    user_products = {}
    if user_id in user_products:
        user_products[user_id].append(product)
    else:
        user_products[user_id] = [product]
    return True

def update_stock(product_id, new_quantity):
    """ Update the stock quantity of a product. """
    product_stock = {}
    if product_id in product_stock:
        product_stock[product_id] = new_quantity
        return True
    else:
        return False

def purchase_product(product_id, buyer_id, quantity):
    """ Handle a purchase between a buyer and a seller for a given product """
    product_stock = {}
    user_products = {}
    transactions = [] 
    if product_id in product_stock:
        if product_stock[product_id] >= quantity:
            product_stock[product_id] -= quantity
            transactions.append({'product_id': product_id, 'buyer_id': buyer_id, 'quantity': quantity})
            
            if buyer_id in user_products:
                purchased_product = {'product_id': product_id, 'quantity': quantity}
                user_products[buyer_id].append(purchased_product)
            else:
                user_products[buyer_id] = [{'product_id': product_id, 'quantity': quantity}]
            return True
        else:
            return False
    else:
        return False

def remove_product(product_id):
    """ Remove a product from a user. """
    user_products = {}
    for user_id, products in user_products.items():
        for product in products:
            if product.get('product_id') == product_id:
                user_products[user_id].remove(product)
                return True
    return False

if __name__ == "__main__":
    # Code to execute if script is run directly
    pass