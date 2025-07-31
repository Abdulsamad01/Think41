# Think41 E-commerce Products API Documentation

## Overview

This RESTful API provides access to product data from the Think41 e-commerce database. The API is built with Flask and supports CORS for frontend integration.

**Base URL:** `http://localhost:5000/api`

## Authentication

Currently, no authentication is required for API access.

## Response Format

All API responses are returned in JSON format with the following structure:

### Success Response
```json
{
  "data": "...",
  "pagination": "...", // if applicable
  "filters": "..." // if applicable
}
```

### Error Response
```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

## HTTP Status Codes

- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

## Endpoints

### 1. Health Check

**GET** `/api/health`

Check if the API is running and database is connected.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "database": "connected"
}
```

---

### 2. Get All Products

**GET** `/api/products`

Retrieve all products with pagination and filtering options.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page, max 100 (default: 20)
- `category` (optional): Filter by product category
- `brand` (optional): Filter by product brand
- `department` (optional): Filter by product department
- `min_price` (optional): Minimum price filter
- `max_price` (optional): Maximum price filter
- `search` (optional): Search in name, brand, or category

**Example Requests:**
```bash
# Get first 20 products
GET /api/products

# Get products with pagination
GET /api/products?page=2&per_page=10

# Filter by category
GET /api/products?category=Jeans

# Filter by price range
GET /api/products?min_price=50&max_price=100

# Search for products
GET /api/products?search=nike

# Combine filters
GET /api/products?category=Jeans&brand=Levi's&min_price=50&page=1&per_page=5
```

**Response:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Seven7 Women's Long Sleeve Stretch",
      "brand": "Seven7",
      "category": "Tops & Tees",
      "department": "Women",
      "retail_price": 49.0,
      "cost": 24.5,
      "sku": "ABC123",
      "distribution_center_id": 1,
      "distribution_center_name": "Chicago IL"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_count": 29120,
    "total_pages": 1456,
    "has_next": true,
    "has_prev": false
  },
  "filters": {
    "category": "Jeans",
    "brand": null,
    "department": null,
    "min_price": null,
    "max_price": null,
    "search": null
  }
}
```

---

### 3. Get Product by ID

**GET** `/api/products/{id}`

Retrieve a specific product by its ID.

**Path Parameters:**
- `id` (required): Product ID

**Example Request:**
```bash
GET /api/products/1
```

**Success Response (200):**
```json
{
  "product": {
    "id": 1,
    "name": "Seven7 Women's Long Sleeve Stretch",
    "brand": "Seven7",
    "category": "Tops & Tees",
    "department": "Women",
    "retail_price": 49.0,
    "cost": 24.5,
    "sku": "ABC123",
    "distribution_center_id": 1,
    "distribution_center_name": "Chicago IL"
  }
}
```

**Error Response (404):**
```json
{
  "error": "Product not found",
  "message": "No product found with ID 999999"
}
```

---

### 4. Get Product Categories

**GET** `/api/products/categories`

Retrieve all product categories with statistics.

**Response:**
```json
{
  "categories": [
    {
      "category": "Intimates",
      "count": 2363,
      "avg_price": 25.50,
      "min_price": 5.99,
      "max_price": 89.99
    }
  ],
  "total_categories": 25
}
```

---

### 5. Get Product Brands

**GET** `/api/products/brands`

Retrieve all product brands with statistics (limited to top 50).

**Response:**
```json
{
  "brands": [
    {
      "brand": "Nike",
      "count": 1250,
      "avg_price": 75.30
    }
  ],
  "total_brands": 50
}
```

---

### 6. Get Product Departments

**GET** `/api/products/departments`

Retrieve all product departments with statistics.

**Response:**
```json
{
  "departments": [
    {
      "department": "Women",
      "count": 15000,
      "avg_price": 45.20
    }
  ],
  "total_departments": 3
}
```

---

### 7. Get Product Statistics

**GET** `/api/products/stats`

Retrieve comprehensive product statistics and price distribution.

**Response:**
```json
{
  "statistics": {
    "total_products": 29120,
    "total_categories": 25,
    "total_brands": 150,
    "total_departments": 3,
    "avg_price": 52.45,
    "min_price": 5.99,
    "max_price": 999.00,
    "premium_products": 8500
  },
  "price_distribution": [
    {
      "price_range": "Under $25",
      "count": 8500
    },
    {
      "price_range": "$25-$50",
      "count": 12000
    },
    {
      "price_range": "$50-$100",
      "count": 6500
    },
    {
      "price_range": "$100-$200",
      "count": 1500
    },
    {
      "price_range": "Over $200",
      "count": 620
    }
  ]
}
```

## Usage Examples

### Frontend Integration (JavaScript)

```javascript
// Get all products
fetch('http://localhost:5000/api/products')
  .then(response => response.json())
  .then(data => {
    console.log('Products:', data.products);
    console.log('Total:', data.pagination.total_count);
  });

// Get specific product
fetch('http://localhost:5000/api/products/1')
  .then(response => response.json())
  .then(data => {
    console.log('Product:', data.product);
  });

// Search products
fetch('http://localhost:5000/api/products?search=nike&category=Active')
  .then(response => response.json())
  .then(data => {
    console.log('Search results:', data.products);
  });
```

### cURL Examples

```bash
# Health check
curl http://localhost:5000/api/health

# Get products with pagination
curl "http://localhost:5000/api/products?page=1&per_page=10"

# Get product by ID
curl http://localhost:5000/api/products/1

# Filter by category
curl "http://localhost:5000/api/products?category=Jeans"

# Get categories
curl http://localhost:5000/api/products/categories

# Get statistics
curl http://localhost:5000/api/products/stats
```

### Postman Collection

You can import these endpoints into Postman:

1. **Health Check**: `GET http://localhost:5000/api/health`
2. **Get Products**: `GET http://localhost:5000/api/products`
3. **Get Product by ID**: `GET http://localhost:5000/api/products/1`
4. **Get Categories**: `GET http://localhost:5000/api/products/categories`
5. **Get Brands**: `GET http://localhost:5000/api/products/brands`
6. **Get Departments**: `GET http://localhost:5000/api/products/departments`
7. **Get Stats**: `GET http://localhost:5000/api/products/stats`

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- **400 Bad Request**: Invalid query parameters
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side error

## Rate Limiting

Currently, no rate limiting is implemented.

## CORS

CORS is enabled for all origins to support frontend integration.

## Database Schema

The API connects to a SQLite database with the following product table structure:

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    cost DECIMAL(10, 2),
    category VARCHAR(100),
    name TEXT NOT NULL,
    brand VARCHAR(100),
    retail_price DECIMAL(10, 2),
    department VARCHAR(50),
    sku VARCHAR(100),
    distribution_center_id INTEGER,
    FOREIGN KEY (distribution_center_id) REFERENCES distribution_centers(id)
);
```

## Testing

Use the provided `test_api.py` script to test all endpoints:

```bash
python test_api.py
```

## Setup and Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure the database exists:
   ```bash
   python load_data_improved.py
   ```

3. Start the API:
   ```bash
   python app.py
   ```

4. Test the API:
   ```bash
   python test_api.py
   ```

The API will be available at `http://localhost:5000` 