import sqlite3

def run_sample_queries():
    """Run sample queries to verify the database and demonstrate functionality"""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    print("=== E-commerce Database Query Results ===\n")
    
    # 1. Total records in each table
    print("1. RECORD COUNTS:")
    tables = ['distribution_centers', 'users', 'products', 'orders', 'inventory_items', 'order_items']
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        print(f"   {table}: {count:,} records")
    
    print("\n" + "="*50)
    
    # 2. Top 5 products by retail price
    print("\n2. TOP 5 MOST EXPENSIVE PRODUCTS:")
    cursor.execute('''
        SELECT id, name, brand, retail_price, category
        FROM products 
        WHERE retail_price IS NOT NULL
        ORDER BY retail_price DESC 
        LIMIT 5
    ''')
    products = cursor.fetchall()
    for product in products:
        print(f"   ID: {product[0]}, Name: {product[1][:40]}..., Brand: {product[2]}, Price: ${product[3]:.2f}, Category: {product[4]}")
    
    print("\n" + "="*50)
    
    # 3. Product categories with count
    print("\n3. PRODUCT CATEGORIES:")
    cursor.execute('''
        SELECT category, COUNT(*) as count
        FROM products 
        WHERE category IS NOT NULL
        GROUP BY category 
        ORDER BY count DESC
        LIMIT 10
    ''')
    categories = cursor.fetchall()
    for category in categories:
        print(f"   {category[0]}: {category[1]:,} products")
    
    print("\n" + "="*50)
    
    # 4. Order status distribution
    print("\n4. ORDER STATUS DISTRIBUTION:")
    cursor.execute('''
        SELECT status, COUNT(*) as count
        FROM orders 
        WHERE status IS NOT NULL
        GROUP BY status 
        ORDER BY count DESC
    ''')
    statuses = cursor.fetchall()
    for status in statuses:
        print(f"   {status[0]}: {status[1]:,} orders")
    
    print("\n" + "="*50)
    
    # 5. Top 5 users by number of orders
    print("\n5. TOP 5 USERS BY ORDER COUNT:")
    cursor.execute('''
        SELECT u.id, u.first_name, u.last_name, COUNT(o.order_id) as order_count
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        GROUP BY u.id, u.first_name, u.last_name
        ORDER BY order_count DESC
        LIMIT 5
    ''')
    users = cursor.fetchall()
    for user in users:
        print(f"   User ID: {user[0]}, Name: {user[1]} {user[2]}, Orders: {user[3]}")
    
    print("\n" + "="*50)
    
    # 6. Distribution centers with their product counts
    print("\n6. DISTRIBUTION CENTERS AND PRODUCT COUNTS:")
    cursor.execute('''
        SELECT dc.id, dc.name, COUNT(p.id) as product_count
        FROM distribution_centers dc
        LEFT JOIN products p ON dc.id = p.distribution_center_id
        GROUP BY dc.id, dc.name
        ORDER BY product_count DESC
    ''')
    centers = cursor.fetchall()
    for center in centers:
        print(f"   {center[1]}: {center[2]:,} products")
    
    print("\n" + "="*50)
    
    # 7. Average order value
    print("\n7. AVERAGE ORDER VALUE:")
    cursor.execute('''
        SELECT AVG(oi.sale_price) as avg_order_value
        FROM order_items oi
        WHERE oi.sale_price IS NOT NULL
    ''')
    avg_value = cursor.fetchone()[0]
    print(f"   Average order value: ${avg_value:.2f}")
    
    print("\n" + "="*50)
    
    # 8. Sample of recent orders
    print("\n8. SAMPLE OF RECENT ORDERS:")
    cursor.execute('''
        SELECT o.order_id, u.first_name, u.last_name, o.status, o.num_of_item, o.created_at
        FROM orders o
        LEFT JOIN users u ON o.user_id = u.id
        WHERE o.created_at IS NOT NULL
        ORDER BY o.created_at DESC
        LIMIT 5
    ''')
    orders = cursor.fetchall()
    for order in orders:
        print(f"   Order {order[0]}: {order[1]} {order[2]} - {order[3]} - {order[4]} items - {order[5]}")
    
    conn.close()

if __name__ == "__main__":
    run_sample_queries() 