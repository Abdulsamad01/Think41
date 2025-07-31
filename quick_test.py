import requests
import json
import time

def test_api():
    base_url = "http://localhost:5000/api"
    
    print("🔍 Testing Think41 E-commerce API...")
    
    # Test health endpoint
    try:
        print("\n1. Testing Health Check...")
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"Response: {response.json()}")
        else:
            print("❌ Health check failed!")
            return False
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")
        print("Make sure the Flask server is running: python app.py")
        return False
    
    # Test products endpoint
    try:
        print("\n2. Testing Products Endpoint...")
        response = requests.get(f"{base_url}/products?per_page=3", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['pagination']['total_count']} total products")
            print(f"Showing {len(data['products'])} products on this page")
            if data['products']:
                first_product = data['products'][0]
                print(f"Sample: {first_product['name'][:50]}... (${first_product['retail_price']})")
        else:
            print("❌ Products endpoint failed!")
            return False
    except Exception as e:
        print(f"❌ Error testing products: {e}")
        return False
    
    # Test specific product endpoint
    try:
        print("\n3. Testing Specific Product...")
        response = requests.get(f"{base_url}/products/1", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            product = response.json()['product']
            print(f"✅ Product found: {product['name'][:50]}...")
        else:
            print("❌ Specific product endpoint failed!")
            return False
    except Exception as e:
        print(f"❌ Error testing specific product: {e}")
        return False
    
    print("\n🎉 All basic tests passed! Your API is working correctly.")
    return True

if __name__ == "__main__":
    test_api() 