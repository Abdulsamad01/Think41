# Think41 E-commerce Database Project

## Milestone 1: Database Design and Loading Data

This project successfully sets up a comprehensive e-commerce database using SQLite and loads data from the e-commerce dataset.

### Project Structure

```
Think41/
├── archive/                          # Original CSV data files
│   ├── distribution_centers.csv      # 10 distribution centers
│   ├── users.csv                     # 100,000 user records
│   ├── products.csv                  # 29,120 product records
│   ├── orders.csv                    # 125,226 order records
│   ├── inventory_items.csv           # 490,705 inventory items
│   └── order_items.csv               # 181,759 order items
├── database_schema.sql               # SQL database schema
├── load_data_improved.py             # Data loading script
├── query_database.py                 # Sample queries and verification
├── examine_csv_simple.py             # CSV structure analysis
├── ecommerce.db                      # SQLite database file (generated)
└── README.md                         # This file
```

### Database Schema

The database consists of 6 main tables with proper relationships:

1. **distribution_centers** - Warehouse locations
2. **users** - Customer information
3. **products** - Product catalog
4. **orders** - Order headers
5. **inventory_items** - Individual inventory units
6. **order_items** - Order line items

### Key Features

- **Proper Foreign Key Relationships**: All tables are properly linked
- **Indexes**: Performance indexes on frequently queried columns
- **Data Validation**: Robust error handling during data loading
- **Progress Tracking**: Real-time progress updates during loading
- **Data Verification**: Comprehensive verification queries

### Data Loading Results

Successfully loaded:
- **10 distribution centers** across different locations
- **100,000 users** with complete profile information
- **29,120 products** across various categories
- **125,226 orders** with status tracking
- **490,705 inventory items** for stock management
- **181,759 order items** linking orders to products

### Sample Data Insights

- **Top Product Categories**: Intimates (2,363), Jeans (1,999), Tops & Tees (1,868)
- **Most Expensive Product**: Alpha Industries Rip Stop Short at $999.00
- **Average Order Value**: Calculated from sale prices
- **Geographic Distribution**: Users and distribution centers across multiple locations

### Usage

1. **Create Database**: Run `python load_data_improved.py` to create and populate the database
2. **Query Data**: Run `python query_database.py` to see sample queries and data verification
3. **Direct SQL**: Use any SQLite client to connect to `ecommerce.db`

### Database Connection

```python
import sqlite3
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()
```

### Sample Queries

The `query_database.py` script demonstrates:
- Record counts for all tables
- Top products by price
- Product category distribution
- Order status analysis
- User order patterns
- Distribution center product counts
- Average order values
- Recent order samples

### Technical Details

- **Database**: SQLite 3
- **Encoding**: UTF-8
- **Error Handling**: Comprehensive exception handling
- **Performance**: Indexed queries for optimal performance
- **Data Types**: Proper data type mapping from CSV to SQL

### Next Steps

This database is now ready for:
- Business intelligence queries
- Analytics and reporting
- Application development
- Data analysis and insights

The foundation is solid for building e-commerce analytics, customer insights, inventory management, and order processing systems.

