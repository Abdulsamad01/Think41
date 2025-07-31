from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
DATABASE = 'ecommerce.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def dict_from_row(row):
    """Convert sqlite3.Row object to dictionary"""
    return dict(zip(row.keys(), row))

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected' if os.path.exists(DATABASE) else 'not found'
    }), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with pagination and filtering"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category = request.args.get('category')
        brand = request.args.get('brand')
        department = request.args.get('department')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        search = request.args.get('search')
        
        # Validate pagination parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
            
        offset = (page - 1) * per_page
        
        conn = get_db_connection()
        
        # Build the WHERE clause based on filters
        where_conditions = []
        params = []
        
        if category:
            where_conditions.append("category = ?")
            params.append(category)
            
        if brand:
            where_conditions.append("brand = ?")
            params.append(brand)
            
        if department:
            where_conditions.append("department = ?")
            params.append(department)
            
        if min_price is not None:
            where_conditions.append("retail_price >= ?")
            params.append(min_price)
            
        if max_price is not None:
            where_conditions.append("retail_price <= ?")
            params.append(max_price)
            
        if search:
            where_conditions.append("(name LIKE ? OR brand LIKE ? OR category LIKE ?)")
            search_term = f"%{search}%"
            params.extend([search_term, search_term, search_term])
        
        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
        
        # Get total count for pagination
        count_query = f"SELECT COUNT(*) as total FROM products WHERE {where_clause}"
        cursor = conn.execute(count_query, params)
        total_count = cursor.fetchone()['total']
        
        # Get products with pagination
        query = f"""
            SELECT p.*, dc.name as distribution_center_name
            FROM products p
            LEFT JOIN distribution_centers dc ON p.distribution_center_id = dc.id
            WHERE {where_clause}
            ORDER BY p.id
            LIMIT ? OFFSET ?
        """
        params.extend([per_page, offset])
        
        cursor = conn.execute(query, params)
        products = [dict_from_row(row) for row in cursor.fetchall()]
        
        # Calculate pagination info
        total_pages = (total_count + per_page - 1) // per_page
        has_next = page < total_pages
        has_prev = page > 1
        
        conn.close()
        
        return jsonify({
            'products': products,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': total_pages,
                'has_next': has_next,
                'has_prev': has_prev
            },
            'filters': {
                'category': category,
                'brand': brand,
                'department': department,
                'min_price': min_price,
                'max_price': max_price,
                'search': search
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    try:
        conn = get_db_connection()
        
        query = """
            SELECT p.*, dc.name as distribution_center_name
            FROM products p
            LEFT JOIN distribution_centers dc ON p.distribution_center_id = dc.id
            WHERE p.id = ?
        """
        
        cursor = conn.execute(query, (product_id,))
        product = cursor.fetchone()
        
        conn.close()
        
        if product is None:
            return jsonify({
                'error': 'Product not found',
                'message': f'No product found with ID {product_id}'
            }), 404
        
        return jsonify({
            'product': dict_from_row(product)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/products/categories', methods=['GET'])
def get_categories():
    """Get all product categories with counts"""
    try:
        conn = get_db_connection()
        
        query = """
            SELECT category, COUNT(*) as count,
                   AVG(retail_price) as avg_price,
                   MIN(retail_price) as min_price,
                   MAX(retail_price) as max_price
            FROM products
            WHERE category IS NOT NULL
            GROUP BY category
            ORDER BY count DESC
        """
        
        cursor = conn.execute(query)
        categories = [dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'categories': categories,
            'total_categories': len(categories)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/products/brands', methods=['GET'])
def get_brands():
    """Get all product brands with counts"""
    try:
        conn = get_db_connection()
        
        query = """
            SELECT brand, COUNT(*) as count,
                   AVG(retail_price) as avg_price
            FROM products
            WHERE brand IS NOT NULL
            GROUP BY brand
            ORDER BY count DESC
            LIMIT 50
        """
        
        cursor = conn.execute(query)
        brands = [dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'brands': brands,
            'total_brands': len(brands)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/products/departments', methods=['GET'])
def get_departments():
    """Get all product departments with counts"""
    try:
        conn = get_db_connection()
        
        query = """
            SELECT department, COUNT(*) as count,
                   AVG(retail_price) as avg_price
            FROM products
            WHERE department IS NOT NULL
            GROUP BY department
            ORDER BY count DESC
        """
        
        cursor = conn.execute(query)
        departments = [dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'departments': departments,
            'total_departments': len(departments)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/products/stats', methods=['GET'])
def get_product_stats():
    """Get product statistics"""
    try:
        conn = get_db_connection()
        
        # Basic stats
        stats_query = """
            SELECT 
                COUNT(*) as total_products,
                COUNT(DISTINCT category) as total_categories,
                COUNT(DISTINCT brand) as total_brands,
                COUNT(DISTINCT department) as total_departments,
                AVG(retail_price) as avg_price,
                MIN(retail_price) as min_price,
                MAX(retail_price) as max_price,
                SUM(CASE WHEN retail_price > 100 THEN 1 ELSE 0 END) as premium_products
            FROM products
            WHERE retail_price IS NOT NULL
        """
        
        cursor = conn.execute(stats_query)
        stats = dict_from_row(cursor.fetchone())
        
        # Price distribution
        price_dist_query = """
            SELECT 
                CASE 
                    WHEN retail_price < 25 THEN 'Under $25'
                    WHEN retail_price < 50 THEN '$25-$50'
                    WHEN retail_price < 100 THEN '$50-$100'
                    WHEN retail_price < 200 THEN '$100-$200'
                    ELSE 'Over $200'
                END as price_range,
                COUNT(*) as count
            FROM products
            WHERE retail_price IS NOT NULL
            GROUP BY price_range
            ORDER BY MIN(retail_price)
        """
        
        cursor = conn.execute(price_dist_query)
        price_distribution = [dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'statistics': stats,
            'price_distribution': price_distribution
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({
        'error': 'Bad request',
        'message': 'Invalid request parameters'
    }), 400

if __name__ == '__main__':
    # Check if database exists
    if not os.path.exists(DATABASE):
        print(f"❌ Error: Database file '{DATABASE}' not found!")
        print("Please run the data loading script first.")
        exit(1)
    
    print("🚀 Starting Think41 E-commerce Products API...")
    print(f"📊 Database: {DATABASE}")
    print("🌐 API will be available at: http://localhost:5000")
    print("📖 API Documentation:")
    print("  - GET /api/health - Health check")
    print("  - GET /api/products - List all products (with pagination)")
    print("  - GET /api/products/{id} - Get specific product")
    print("  - GET /api/products/categories - Get all categories")
    print("  - GET /api/products/brands - Get all brands")
    print("  - GET /api/products/departments - Get all departments")
    print("  - GET /api/products/stats - Get product statistics")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 