import json
import csv
import os
import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker
fake = Faker()

# Configuration
NUM_PRODUCTS = 50
NUM_POS = 15  # Increased from 5 to 15 stores
NUM_WAREHOUSES = 5  # Increased from 2 to 5 warehouses
DAYS_TO_GENERATE = 7  # Generate 7 days of data
OUTPUT_DIR_ORDERS = "data/raw/orders"
OUTPUT_DIR_STOCK = "data/raw/stock"

# Ensure output directories exist
os.makedirs(OUTPUT_DIR_ORDERS, exist_ok=True)
os.makedirs(OUTPUT_DIR_STOCK, exist_ok=True)

# Generate Product IDs (SKUs)
product_ids = [f"SKU-{i:04d}" for i in range(1, NUM_PRODUCTS + 1)]

def generate_pos_orders(date_str):
    """Generate JSON files for POS orders."""
    for pos_id in range(1, NUM_POS + 1):
        orders = []
        num_orders = random.randint(150, 300)  # Much more orders per store
        
        for _ in range(num_orders):
            order = {
                "order_id": fake.uuid4(),
                "pos_id": f"POS-{pos_id:03d}",
                "timestamp": f"{date_str}T{fake.time()}",
                "items": []
            }
            
            num_items = random.randint(1, 8)  # More items per order
            for _ in range(num_items):
                item = {
                    "sku": random.choice(product_ids),
                    "quantity": random.randint(1, 15),  # Higher quantities
                    "price": round(random.uniform(1.0, 150.0), 2)
                }
                order["items"].append(item)
            orders.append(order)
            
        # Save to JSON
        filename = f"{OUTPUT_DIR_ORDERS}/pos_{pos_id}_{date_str}.json"
        with open(filename, 'w') as f:
            json.dump(orders, f, indent=2)
        print(f"Generated {filename}")

def generate_warehouse_stock(date_str):
    """Generate CSV files for Warehouse stock snapshots."""
    for wh_id in range(1, NUM_WAREHOUSES + 1):
        filename = f"{OUTPUT_DIR_STOCK}/wh_{wh_id}_{date_str}.csv"
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["warehouse_id", "date", "sku", "quantity_on_hand"])
            
            for sku in product_ids:
                # Random stock level
                qty = random.randint(0, 500)
                writer.writerow([f"WH-{wh_id:03d}", date_str, sku, qty])
        print(f"Generated {filename}")

if __name__ == "__main__":
    from datetime import timedelta
    
    # Generate data for the last DAYS_TO_GENERATE days
    base_date = datetime.now()
    
    for day_offset in range(DAYS_TO_GENERATE):
        current_date = base_date - timedelta(days=DAYS_TO_GENERATE - day_offset - 1)
        date_str = current_date.strftime("%Y-%m-%d")
        print(f"\nGenerating data for {date_str}...")
        
        generate_pos_orders(date_str)
        generate_warehouse_stock(date_str)
    
    print(f"\nData generation complete! Generated {DAYS_TO_GENERATE} days of data.")
