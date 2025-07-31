import csv
import os

def examine_csv_structure():
    csv_files = [
        'archive/products.csv',
        'archive/users.csv', 
        'archive/orders.csv',
        'archive/order_items.csv',
        'archive/inventory_items.csv',
        'archive/distribution_centers.csv'
    ]
    
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            print(f"\n=== {csv_file} ===")
            try:
                with open(csv_file, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    # Get header
                    header = next(reader)
                    print(f"Columns: {header}")
                    
                    # Get first few rows
                    rows = []
                    for i, row in enumerate(reader):
                        if i < 3:  # First 3 data rows
                            rows.append(row)
                        else:
                            break
                    
                    print(f"First 3 data rows:")
                    for i, row in enumerate(rows):
                        print(f"Row {i+1}: {row}")
                    
                    print("-" * 50)
            except Exception as e:
                print(f"Error reading {csv_file}: {e}")

if __name__ == "__main__":
    examine_csv_structure() 