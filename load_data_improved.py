import sqlite3
import csv
import os
from datetime import datetime

def create_database():
    """Create the database and load all CSV data"""
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Read and execute the schema
    with open('database_schema.sql', 'r') as f:
        schema = f.read()
        cursor.executescript(schema)
    
    print("Database schema created successfully!")
    
    # Load data from CSV files
    load_distribution_centers(cursor)
    load_users(cursor)
    load_products(cursor)
    load_orders(cursor)
    load_inventory_items(cursor)
    load_order_items(cursor)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("All data loaded successfully!")

def load_distribution_centers(cursor):
    """Load distribution centers data"""
    print("Loading distribution centers...")
    count = 0
    with open('archive/distribution_centers.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                cursor.execute('''
                    INSERT INTO distribution_centers (id, name, latitude, longitude)
                    VALUES (?, ?, ?, ?)
                ''', (
                    int(row['id']),
                    row['name'],
                    float(row['latitude']) if row['latitude'] else None,
                    float(row['longitude']) if row['longitude'] else None
                ))
                count += 1
            except Exception as e:
                print(f"Error loading distribution center {row['id']}: {e}")
    print(f"Distribution centers loaded: {count} records")

def load_users(cursor):
    """Load users data"""
    print("Loading users...")
    count = 0
    with open('archive/users.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                cursor.execute('''
                    INSERT INTO users (id, first_name, last_name, email, age, gender, 
                                     state, street_address, postal_code, city, country, 
                                     latitude, longitude, traffic_source, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    int(row['id']),
                    row['first_name'],
                    row['last_name'],
                    row['email'],
                    int(row['age']) if row['age'] and row['age'].isdigit() else None,
                    row['gender'],
                    row['state'],
                    row['street_address'],
                    row['postal_code'],
                    row['city'],
                    row['country'],
                    float(row['latitude']) if row['latitude'] else None,
                    float(row['longitude']) if row['longitude'] else None,
                    row['traffic_source'],
                    row['created_at'] if row['created_at'] else None
                ))
                count += 1
                if count % 1000 == 0:
                    print(f"  Loaded {count} users...")
            except Exception as e:
                print(f"Error loading user {row['id']}: {e}")
    print(f"Users loaded: {count} records")

def load_products(cursor):
    """Load products data"""
    print("Loading products...")
    count = 0
    with open('archive/products.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                cursor.execute('''
                    INSERT INTO products (id, cost, category, name, brand, retail_price, 
                                        department, sku, distribution_center_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    int(row['id']),
                    float(row['cost']) if row['cost'] else None,
                    row['category'],
                    row['name'],
                    row['brand'],
                    float(row['retail_price']) if row['retail_price'] else None,
                    row['department'],
                    row['sku'],
                    int(row['distribution_center_id']) if row['distribution_center_id'] and row['distribution_center_id'].isdigit() else None
                ))
                count += 1
                if count % 1000 == 0:
                    print(f"  Loaded {count} products...")
            except Exception as e:
                print(f"Error loading product {row['id']}: {e}")
    print(f"Products loaded: {count} records")

def load_orders(cursor):
    """Load orders data"""
    print("Loading orders...")
    count = 0
    with open('archive/orders.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Handle empty or invalid user_id
                user_id = row['user_id']
                if user_id and user_id.isdigit():
                    user_id = int(user_id)
                else:
                    user_id = None
                    
                cursor.execute('''
                    INSERT INTO orders (order_id, user_id, status, gender, created_at, 
                                      returned_at, shipped_at, delivered_at, num_of_item)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    int(row['order_id']),
                    user_id,
                    row['status'],
                    row['gender'],
                    row['created_at'] if row['created_at'] else None,
                    row['returned_at'] if row['returned_at'] else None,
                    row['shipped_at'] if row['shipped_at'] else None,
                    row['delivered_at'] if row['delivered_at'] else None,
                    int(row['num_of_item']) if row['num_of_item'] and row['num_of_item'].isdigit() else None
                ))
                count += 1
                if count % 1000 == 0:
                    print(f"  Loaded {count} orders...")
            except Exception as e:
                print(f"Error loading order {row['order_id']}: {e}")
    print(f"Orders loaded: {count} records")

def load_inventory_items(cursor):
    """Load inventory items data"""
    print("Loading inventory items...")
    count = 0
    with open('archive/inventory_items.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                cursor.execute('''
                    INSERT INTO inventory_items (id, product_id, created_at, sold_at, cost,
                                               product_category, product_name, product_brand,
                                               product_retail_price, product_department,
                                               product_sku, product_distribution_center_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    int(row['id']),
                    int(row['product_id']) if row['product_id'] and row['product_id'].isdigit() else None,
                    row['created_at'] if row['created_at'] else None,
                    row['sold_at'] if row['sold_at'] else None,
                    float(row['cost']) if row['cost'] else None,
                    row['product_category'],
                    row['product_name'],
                    row['product_brand'],
                    float(row['product_retail_price']) if row['product_retail_price'] else None,
                    row['product_department'],
                    row['product_sku'],
                    int(row['product_distribution_center_id']) if row['product_distribution_center_id'] and row['product_distribution_center_id'].isdigit() else None
                ))
                count += 1
                if count % 5000 == 0:
                    print(f"  Loaded {count} inventory items...")
            except Exception as e:
                print(f"Error loading inventory item {row['id']}: {e}")
    print(f"Inventory items loaded: {count} records")

def load_order_items(cursor):
    """Load order items data"""
    print("Loading order items...")
    count = 0
    with open('archive/order_items.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                cursor.execute('''
                    INSERT INTO order_items (id, order_id, user_id, product_id, inventory_item_id,
                                           status, created_at, shipped_at, delivered_at, returned_at, sale_price)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    int(row['id']),
                    int(row['order_id']) if row['order_id'] and row['order_id'].isdigit() else None,
                    int(row['user_id']) if row['user_id'] and row['user_id'].isdigit() else None,
                    int(row['product_id']) if row['product_id'] and row['product_id'].isdigit() else None,
                    int(row['inventory_item_id']) if row['inventory_item_id'] and row['inventory_item_id'].isdigit() else None,
                    row['status'],
                    row['created_at'] if row['created_at'] else None,
                    row['shipped_at'] if row['shipped_at'] else None,
                    row['delivered_at'] if row['delivered_at'] else None,
                    row['returned_at'] if row['returned_at'] else None,
                    float(row['sale_price']) if row['sale_price'] else None
                ))
                count += 1
                if count % 5000 == 0:
                    print(f"  Loaded {count} order items...")
            except Exception as e:
                print(f"Error loading order item {row['id']}: {e}")
    print(f"Order items loaded: {count} records")

def verify_data():
    """Verify that data was loaded correctly"""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    print("\n=== Data Verification ===")
    
    # Check record counts
    tables = ['distribution_centers', 'users', 'products', 'orders', 'inventory_items', 'order_items']
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        print(f"{table}: {count} records")
    
    # Sample queries
    print("\n=== Sample Data ===")
    
    # Sample products
    cursor.execute('SELECT id, name, brand, retail_price FROM products LIMIT 5')
    products = cursor.fetchall()
    print("Sample Products:")
    for product in products:
        print(f"  ID: {product[0]}, Name: {product[1][:50]}..., Brand: {product[2]}, Price: ${product[3]}")
    
    # Sample users
    cursor.execute('SELECT id, first_name, last_name, email FROM users LIMIT 5')
    users = cursor.fetchall()
    print("\nSample Users:")
    for user in users:
        print(f"  ID: {user[0]}, Name: {user[1]} {user[2]}, Email: {user[3]}")
    
    # Sample orders
    cursor.execute('SELECT order_id, user_id, status, num_of_item FROM orders LIMIT 5')
    orders = cursor.fetchall()
    print("\nSample Orders:")
    for order in orders:
        print(f"  Order ID: {order[0]}, User ID: {order[1]}, Status: {order[2]}, Items: {order[3]}")
    
    conn.close()

if __name__ == "__main__":
    create_database()
    verify_data() 