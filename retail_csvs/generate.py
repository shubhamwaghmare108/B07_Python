#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
generate_transactions.py

Reads customers.csv, brands.csv, categories.csv and generates:
- orders.csv (5000 rows)
- order_items.csv (approximately 15,000 rows)

Usage:
    python generate_transactions.py
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ------------------------------
# CONFIGURATION
# ------------------------------
NUM_ORDERS = 5000
MIN_ITEMS_PER_ORDER = 1
MAX_ITEMS_PER_ORDER = 5

PAYMENT_METHODS = ['UPI', 'Card', 'COD', 'NetBanking']
ORDER_STATUSES = ['Delivered', 'Shipped', 'Pending', 'Cancelled']
STATUS_WEIGHTS = [0.75, 0.10, 0.10, 0.05]

# Price range per category (just for realism)
CATEGORY_PRICE_RANGES = {
    # Personal Care
    79: (50, 250),   # Toothpaste
    80: (80, 400),   # Face Wash
    91: (30, 150),   # Bar Soap
    94: (100, 500),  # Face Cream
    96: (60, 200),   # Toothbrush
    101: (150, 600), # Conditioner
    115: (50, 200),  # Hand Wash
    121: (100, 300), # Mouthwash
    126: (80, 300),  # Body Wash
    131: (80, 250),  # Hair Oil
    141: (120, 350), # Spray Deodorant
    147: (100, 250), # Roll-on Deodorant
    178: (80, 350),  # Shampoo
    184: (100, 400), # Body Lotion
    # Dairy & Bakery
    81: (30, 60),    # Toned Milk
    85: (40, 80),    # Full Cream Milk
    86: (20, 40),    # Pav
    97: (30, 60),    # Brown Bread
    100: (20, 50),   # Buttermilk
    111: (25, 50),   # White Bread
    128: (150, 400), # Cheese Block
    139: (80, 200),  # Paneer
    169: (80, 200),  # Butter
    175: (20, 40),   # Buns
    183: (60, 150),  # Cheese Slices
    193: (30, 70),   # Curd
    # Groceries & Staples
    82: (30, 70),    # Sooji
    92: (60, 150),   # Rajma
    98: (30, 80),    # Turmeric Powder
    103: (20, 50),   # Iodized Salt
    108: (70, 150),  # Urad Dal
    114: (30, 80),   # Chilli Powder
    124: (80, 200),  # Mustard Oil
    129: (25, 50),   # Maida
    132: (70, 150),  # Sona Masoori Rice
    142: (100, 250), # Basmati Rice
    151: (80, 180),  # Brown Rice
    155: (60, 140),  # Chana Dal
    156: (60, 140),  # Toor Dal
    160: (30, 70),   # Besan
    162: (30, 60),   # Sugar
    170: (70, 150),  # Moong Dal
    171: (150, 400), # Olive Oil
    174: (30, 80),   # Coriander Powder
    179: (30, 70),   # Rock Salt
    182: (40, 90),   # Whole Wheat Atta
    190: (40, 100),  # Garam Masala
    194: (100, 250), # Groundnut Oil
    195: (100, 250), # Sunflower Oil
    # Snacks & Confectionery
    83: (10, 30),    # Mints
    84: (30, 70),    # Khakra
    87: (80, 200),   # Strawberry Ice Cream
    88: (20, 60),    # Crackers
    102: (30, 80),   # Bhujia
    104: (50, 150),  # Milk Chocolate
    105: (80, 200),  # Dark Chocolate
    107: (80, 200),  # Chocolate Ice Cream
    110: (40, 100),  # Cookies
    116: (10, 30),   # Chewing Gum
    123: (20, 50),   # Toffees
    125: (20, 60),   # Potato Chips
    133: (80, 200),  # Vanilla Ice Cream
    134: (40, 100),  # Digestive
    164: (40, 100),  # Cream Biscuits
    168: (50, 150),  # Wafer Chocolate
    188: (30, 80),   # Mixture
    # Frozen & Non-Veg
    90: (100, 250),  # Veg Cutlet
    113: (150, 400), # Fish
    127: (120, 300), # Chicken
    135: (60, 120),  # Regular Eggs
    136: (80, 150),  # Country Eggs
    144: (70, 130),  # Brown Eggs
    152: (200, 500), # Mutton
    159: (100, 250), # Veg Nuggets
    167: (150, 350), # Chicken Nuggets
    191: (80, 200),  # French Fries
    # Home Care
    89: (50, 150),   # Dishwash Powder
    93: (80, 200),   # Dishwash Liquid
    99: (40, 100),   # Detergent Bar
    109: (100, 250), # Floor Cleaner
    119: (50, 120),  # Dishwash Bar
    120: (80, 200),  # Mosquito Spray
    130: (100, 300), # Detergent Powder
    138: (80, 200),  # Toilet Cleaner
    150: (50, 150),  # Air Freshener Gel
    165: (80, 200),  # Air Freshener Spray
    173: (80, 200),  # Mosquito Liquid
    176: (120, 300), # Detergent Liquid
    177: (60, 150),  # Glass Cleaner
    181: (30, 80),   # Mosquito Coil
    # Beverages
    95: (30, 70),    # Orange Drink
    117: (100, 250), # Green Tea
    122: (80, 180),  # Energy Drink
    140: (60, 150),  # Masala Tea
    143: (50, 120),  # Mixed Fruit Juice
    145: (50, 120),  # Apple Juice
    148: (150, 350), # Instant Coffee
    149: (30, 70),   # Cola
    154: (30, 70),   # Lemon Drink
    161: (60, 150),  # Black Tea
    180: (80, 180),  # Cold Coffee
    185: (20, 50),   # Mineral Water
    186: (50, 120),  # Orange Juice
    187: (50, 120),  # Mango Juice
    196: (100, 250), # Filter Coffee
    # Fruits & Vegetables
    106: (20, 50),   # Cabbage
    112: (80, 200),  # Grapes
    118: (80, 200),  # Bell Pepper
    137: (20, 50),   # Potato
    146: (80, 200),  # Zucchini
    153: (30, 70),   # Banana
    157: (50, 120),  # Orange
    158: (100, 250), # Broccoli
    163: (30, 70),   # Tomato
    166: (20, 50),   # Onion
    172: (80, 200),  # Apple
    189: (30, 70),   # Cauliflower
    192: (80, 200),  # Mango
}

# ------------------------------
# FUNCTIONS
# ------------------------------

def load_data():
    """Read the existing CSV files."""
    customers = pd.read_csv('customers.csv')
    brands = pd.read_csv('brands.csv')
    categories = pd.read_csv('categories.csv')
    return customers, brands, categories

def generate_order_date():
    """Generate a random order date in the last 365 days."""
    start = datetime.now() - timedelta(days=365)
    return start + timedelta(days=random.randint(0, 365))

def get_category_price(category_id):
    """Return a realistic price range for a category."""
    # If category not in map, use a generic range
    if category_id in CATEGORY_PRICE_RANGES:
        low, high = CATEGORY_PRICE_RANGES[category_id]
    else:
        low, high = 50, 200
    return round(random.uniform(low, high), 2)

def generate_orders(customers):
    """Generate orders dataframe."""
    customer_ids = customers['customer_id'].tolist()
    orders = []
    order_id = 10001
    for _ in range(NUM_ORDERS):
        cust_id = random.choice(customer_ids)
        order_date = generate_order_date()
        num_items = random.randint(MIN_ITEMS_PER_ORDER, MAX_ITEMS_PER_ORDER)
        # We'll compute total later
        orders.append({
            'order_id': order_id,
            'customer_id': cust_id,
            'order_date': order_date.strftime('%Y-%m-%d'),
            'total_amount': 0.0,  # placeholder
            'payment_method': random.choices(PAYMENT_METHODS, weights=[0.4, 0.3, 0.2, 0.1])[0],
            'order_status': random.choices(ORDER_STATUSES, weights=STATUS_WEIGHTS)[0]
        })
        order_id += 1
    return pd.DataFrame(orders)

def generate_order_items(orders, brands, categories):
    """Generate order_items dataframe and update order totals."""
    # Get lists of ids
    brand_ids = brands['brand_id'].tolist()
    category_ids = categories['category_id'].tolist()
    
    order_items = []
    item_id = 1
    order_totals = {row['order_id']: 0.0 for _, row in orders.iterrows()}
    
    for _, order in orders.iterrows():
        order_id = order['order_id']
        num_items = random.randint(MIN_ITEMS_PER_ORDER, MAX_ITEMS_PER_ORDER)
        # Pick distinct combinations to avoid exact duplicates (optional)
        for _ in range(num_items):
            brand_id = random.choice(brand_ids)
            category_id = random.choice(category_ids)
            quantity = random.randint(1, 3)
            unit_price = get_category_price(category_id)
            line_total = quantity * unit_price
            order_totals[order_id] += line_total
            
            order_items.append({
                'item_id': item_id,
                'order_id': order_id,
                'brand_id': brand_id,
                'category_id': category_id,
                'quantity': quantity,
                'unit_price': round(unit_price, 2)
            })
            item_id += 1
    
    # Update order totals
    orders['total_amount'] = orders['order_id'].map(order_totals).round(2)
    return pd.DataFrame(order_items)

def main():
    print("Loading existing data...")
    customers, brands, categories = load_data()
    print(f"Loaded {len(customers)} customers, {len(brands)} brands, {len(categories)} categories.")
    
    print("Generating orders...")
    orders = generate_orders(customers)
    print(f"Generated {len(orders)} orders.")
    
    print("Generating order items...")
    order_items = generate_order_items(orders, brands, categories)
    print(f"Generated {len(order_items)} order items.")
    
    # Save to CSV
    orders.to_csv('orders.csv', index=False)
    order_items.to_csv('order_items.csv', index=False)
    print("✅ Successfully created orders.csv and order_items.csv")
    print("\nSample of orders:")
    print(orders.head())
    print("\nSample of order_items:")
    print(order_items.head())

if __name__ == "__main__":
    main()