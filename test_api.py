import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_products():
    """Test getting all products with pagination"""
    print("\n🔍 Testing Get All Products...")
    try:
        response = requests.get(f"{BASE_URL}/products?page=1&per_page=5")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Total Products: {data['pagination']['total_count']}")
            print(f"Products in this page: {len(data['products'])}")
            print(f"Pagination: Page {data['pagination']['page']} of {data['pagination']['total_pages']}")
            
            # Show first product as sample
            if data['products']:
                first_product = data['products'][0]
                print(f"Sample Product: ID {first_product['id']}, {first_product['name'][:50]}...")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_product_by_id():
    """Test getting a specific product by ID"""
    print("\n🔍 Testing Get Product by ID...")
    try:
        # First get a list of products to get a valid ID
        response = requests.get(f"{BASE_URL}/products?per_page=1")
        if response.status_code == 200:
            products = response.json()['products']
            if products:
                product_id = products[0]['id']
                
                # Test getting the specific product
                response = requests.get(f"{BASE_URL}/products/{product_id}")
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    product = response.json()['product']
                    print(f"Product Found: ID {product['id']}, Name: {product['name'][:50]}...")
                    print(f"Brand: {product['brand']}, Price: ${product['retail_price']}")
                else:
                    print(f"Response: {response.json()}")
                
                return response.status_code == 200
        
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_product_not_found():
    """Test getting a product that doesn't exist"""
    print("\n🔍 Testing Get Product Not Found...")
    try:
        response = requests.get(f"{BASE_URL}/products/999999")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 404
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_categories():
    """Test getting product categories"""
    print("\n🔍 Testing Get Categories...")
    try:
        response = requests.get(f"{BASE_URL}/products/categories")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Total Categories: {data['total_categories']}")
            print("Top 5 Categories:")
            for i, category in enumerate(data['categories'][:5]):
                print(f"  {i+1}. {category['category']}: {category['count']} products")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_brands():
    """Test getting product brands"""
    print("\n🔍 Testing Get Brands...")
    try:
        response = requests.get(f"{BASE_URL}/products/brands")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Total Brands: {data['total_brands']}")
            print("Top 5 Brands:")
            for i, brand in enumerate(data['brands'][:5]):
                print(f"  {i+1}. {brand['brand']}: {brand['count']} products")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_departments():
    """Test getting product departments"""
    print("\n🔍 Testing Get Departments...")
    try:
        response = requests.get(f"{BASE_URL}/products/departments")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Total Departments: {data['total_departments']}")
            print("All Departments:")
            for dept in data['departments']:
                print(f"  - {dept['department']}: {dept['count']} products")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_stats():
    """Test getting product statistics"""
    print("\n🔍 Testing Get Product Stats...")
    try:
        response = requests.get(f"{BASE_URL}/products/stats")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            stats = data['statistics']
            print("Product Statistics:")
            print(f"  Total Products: {stats['total_products']}")
            print(f"  Total Categories: {stats['total_categories']}")
            print(f"  Total Brands: {stats['total_brands']}")
            print(f"  Average Price: ${stats['avg_price']:.2f}")
            print(f"  Price Range: ${stats['min_price']:.2f} - ${stats['max_price']:.2f}")
            print(f"  Premium Products (>$100): {stats['premium_products']}")
            
            print("\nPrice Distribution:")
            for dist in data['price_distribution']:
                print(f"  {dist['price_range']}: {dist['count']} products")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_product_filters():
    """Test product filtering"""
    print("\n🔍 Testing Product Filters...")
    try:
        # Test category filter
        response = requests.get(f"{BASE_URL}/products?category=Jeans&per_page=3")
        print(f"Category Filter (Jeans) - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Found {data['pagination']['total_count']} jeans products")
        
        # Test price filter
        response = requests.get(f"{BASE_URL}/products?min_price=50&max_price=100&per_page=3")
        print(f"Price Filter ($50-$100) - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Found {data['pagination']['total_count']} products in price range")
        
        # Test search
        response = requests.get(f"{BASE_URL}/products?search=nike&per_page=3")
        print(f"Search Filter (nike) - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Found {data['pagination']['total_count']} products matching 'nike'")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("🚀 Starting Think41 E-commerce API Tests...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Get All Products", test_get_products),
        ("Get Product by ID", test_get_product_by_id),
        ("Get Product Not Found", test_get_product_not_found),
        ("Get Categories", test_get_categories),
        ("Get Brands", test_get_brands),
        ("Get Departments", test_get_departments),
        ("Get Product Stats", test_get_stats),
        ("Product Filters", test_product_filters)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            print(f"✅ {test_name} - PASSED")
            passed += 1
        else:
            print(f"❌ {test_name} - FAILED")
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the API implementation.")
    
    return passed == total

if __name__ == "__main__":
    print("Make sure the Flask API is running on http://localhost:5000")
    print("Run: python app.py")
    print("\nStarting tests in 3 seconds...")
    import time
    time.sleep(3)
    
    run_all_tests() 