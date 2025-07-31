import sqlite3
import os

def verify_database_setup():
    """Verify that the database is properly set up and contains all expected data"""
    
    print("=== Think41 E-commerce Database Setup Verification ===\n")
    
    # Check if database file exists
    if not os.path.exists('ecommerce.db'):
        print("❌ ERROR: Database file 'ecommerce.db' not found!")
        return False
    
    db_size = os.path.getsize('ecommerce.db') / (1024 * 1024)  # Size in MB
    print(f"✅ Database file exists: {db_size:.1f} MB")
    
    # Connect to database
    try:
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ ERROR: Cannot connect to database: {e}")
        return False
    
    # Check all tables exist
    expected_tables = ['distribution_centers', 'users', 'products', 'orders', 'inventory_items', 'order_items']
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [row[0] for row in cursor.fetchall()]
    
    print("\n📊 Table Verification:")
    for table in expected_tables:
        if table in existing_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  ✅ {table}: {count:,} records")
        else:
            print(f"  ❌ {table}: NOT FOUND")
            return False
    
    # Verify data integrity with sample queries
    print("\n🔍 Data Integrity Checks:")
    
    # Check for products with valid prices
    cursor.execute("SELECT COUNT(*) FROM products WHERE retail_price > 0")
    valid_products = cursor.fetchone()[0]
    print(f"  ✅ Products with valid prices: {valid_products:,}")
    
    # Check for users with valid emails
    cursor.execute("SELECT COUNT(*) FROM users WHERE email LIKE '%@%'")
    valid_users = cursor.fetchone()[0]
    print(f"  ✅ Users with valid emails: {valid_users:,}")
    
    # Check for orders with valid status
    cursor.execute("SELECT COUNT(*) FROM orders WHERE status IS NOT NULL")
    valid_orders = cursor.fetchone()[0]
    print(f"  ✅ Orders with valid status: {valid_orders:,}")
    
    # Check foreign key relationships
    print("\n🔗 Relationship Checks:")
    
    # Products linked to distribution centers
    cursor.execute("""
        SELECT COUNT(*) FROM products p 
        JOIN distribution_centers dc ON p.distribution_center_id = dc.id
    """)
    linked_products = cursor.fetchone()[0]
    print(f"  ✅ Products linked to distribution centers: {linked_products:,}")
    
    # Orders linked to users
    cursor.execute("""
        SELECT COUNT(*) FROM orders o 
        JOIN users u ON o.user_id = u.id
    """)
    linked_orders = cursor.fetchone()[0]
    print(f"  ✅ Orders linked to users: {linked_orders:,}")
    
    # Sample data verification
    print("\n📋 Sample Data Verification:")
    
    # Sample product
    cursor.execute("SELECT id, name, brand, retail_price FROM products LIMIT 1")
    product = cursor.fetchone()
    if product:
        print(f"  ✅ Sample product: ID {product[0]}, {product[1][:30]}..., Brand: {product[2]}, Price: ${product[3]}")
    
    # Sample user
    cursor.execute("SELECT id, first_name, last_name, email FROM users LIMIT 1")
    user = cursor.fetchone()
    if user:
        print(f"  ✅ Sample user: ID {user[0]}, {user[1]} {user[2]}, Email: {user[3]}")
    
    # Sample order
    cursor.execute("SELECT order_id, user_id, status FROM orders LIMIT 1")
    order = cursor.fetchone()
    if order:
        print(f"  ✅ Sample order: ID {order[0]}, User: {order[1]}, Status: {order[2]}")
    
    conn.close()
    
    print("\n🎉 VERIFICATION COMPLETE!")
    print("✅ Database setup is successful and ready for use!")
    print("\n📝 Next steps:")
    print("  - Run 'python query_database.py' to see sample queries")
    print("  - Use any SQLite client to explore the data")
    print("  - Start building your e-commerce analytics!")
    
    return True

if __name__ == "__main__":
    verify_database_setup() 