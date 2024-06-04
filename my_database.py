# TESTING IN CLI
# RUN: python my_database.py

import sqlite3

conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
''')

def add_user(name):
    cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
    conn.commit()

def create_index():
    cursor.execute('''CREATE INDEX IF NOT EXISTS idx_products_name_description ON products (name, description)''')
    conn.commit()   

def add_product(name, description, price):
    try:
        cursor.execute('''
            ALTER TABLE products 
            ADD COLUMN description TEXT
        ''')
    except sqlite3.OperationalError as e:
        if "duplicate column name" not in str(e):
            raise 
    
    cursor.execute('INSERT INTO products (name, description, price) VALUES (?, ?, ?)', (name, description, price))
    conn.commit()

def get_all_users():
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()

def get_all_products():
    cursor.execute('SELECT * FROM products')
    return cursor.fetchall()

users = [
    'Ray',
    'Alice',
    'Bob',
    'Emma'
]

for user in users:
    add_user(user)

products = [
    ('Sweater', 'Warm and cozy sweater for cold weather', 29.99),
    ('T-Shirt', 'Casual and comfortable cotton t-shirt', 14.99),
    ('Jeans', 'Classic denim jeans for everyday wear', 39.99),
    ('Shoes', 'Stylish and durable shoes for any occasion', 49.99),
    ('Hat', 'Trendy and versatile hat to complete your look', 9.99)
]

for product in products:
    add_product(*product)

print("Users:", get_all_users())
print("Products:", get_all_products())

conn.close()