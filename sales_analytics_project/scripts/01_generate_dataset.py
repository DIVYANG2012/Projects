"""
=============================================================
 Script 01 — Dataset Generator
 Sales Performance Analytics Dashboard | Internship Project
 Generates realistic 50,847 retail sales transaction records
=============================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

# ── Config ────────────────────────────────────────────────────────────────────
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'sales_raw.csv')

CATEGORIES = {
    'Electronics': {
        'weight': 0.38,
        'products': [
            ('65" Smart TV', 58000, 75000),
            ('iPhone 15 Pro', 90000, 130000),
            ('Gaming Laptop', 65000, 95000),
            ('Samsung Galaxy S24', 55000, 80000),
            ('iPad Pro 12.9"', 80000, 115000),
            ('Sony Headphones WH-1000XM5', 18000, 28000),
            ('Wireless Earbuds', 3000, 8000),
            ('Smart Watch Series 9', 25000, 45000),
            ('Air Purifier HEPA', 12000, 22000),
            ('Portable Speaker', 5000, 12000),
            ('Tablet 10"', 15000, 25000),
            ('Webcam 4K', 4000, 8000),
            ('Mechanical Keyboard', 3500, 9000),
            ('Gaming Mouse', 2000, 6000),
            ('Monitor 27" 4K', 22000, 38000),
        ]
    },
    'Apparel': {
        'weight': 0.27,
        'products': [
            ('Running Shoes Premium', 4500, 9500),
            ('Casual Jacket', 2500, 5500),
            ('Formal Shirt', 1200, 2800),
            ('Denim Jeans', 1500, 3500),
            ('Sports T-Shirt', 600, 1400),
            ('Winter Coat', 3500, 7500),
            ('Ethnic Kurta Set', 1800, 4200),
            ('Saree Silk', 3000, 8000),
            ('Sports Shoes', 2800, 6500),
            ('Yoga Pants', 800, 1800),
            ('Formal Trousers', 1400, 3200),
            ('Sandals Casual', 700, 1600),
            ('Woolen Sweater', 1200, 2800),
        ]
    },
    'Home & Living': {
        'weight': 0.21,
        'products': [
            ('Office Chair Ergonomic', 8000, 18000),
            ('Mixer Grinder 750W', 3500, 7500),
            ('Air Conditioner 1.5T', 32000, 48000),
            ('Refrigerator 300L', 22000, 35000),
            ('Washing Machine 7kg', 18000, 28000),
            ('Microwave Oven 25L', 6000, 12000),
            ('Coffee Maker', 4500, 9500),
            ('Yoga Mat Premium', 1200, 2800),
            ('LED Lamp Set', 800, 2200),
            ('Bedsheet King Size', 1500, 4000),
            ('Cookware Set 5pc', 2800, 6500),
            ('Wall Clock Designer', 600, 2000),
        ]
    },
    'Food & Beverages': {
        'weight': 0.14,
        'products': [
            ('Protein Powder 2kg', 2000, 4500),
            ('Organic Honey 500g', 400, 900),
            ('Green Tea Premium 100pc', 600, 1400),
            ('Dry Fruits Gift Box', 800, 2200),
            ('Olive Oil 1L', 500, 1100),
            ('Quinoa 1kg', 300, 700),
            ('Whey Protein Bar 12pc', 700, 1600),
            ('Coffee Beans 500g', 600, 1400),
            ('Herbal Tea Assorted', 400, 950),
            ('Chia Seeds 500g', 350, 750),
        ]
    }
}

REGIONS = ['North', 'South', 'West', 'East', 'Central']
REGION_WEIGHTS = [0.30, 0.25, 0.21, 0.16, 0.08]

SEGMENTS = ['Premium', 'Standard', 'Budget']
SEGMENT_WEIGHTS = [0.15, 0.52, 0.33]

SALES_REPS = [f'SR{str(i).zfill(3)}' for i in range(1, 46)]

# Monthly seasonality multipliers (Jan=low, Nov=high)
MONTHLY_MULT = {
    1: 0.58, 2: 0.68, 3: 0.80, 4: 0.87, 5: 0.92,
    6: 1.00, 7: 1.13, 8: 0.96, 9: 1.08, 10: 1.21,
    11: 1.53, 12: 1.22
}

def generate_dataset(n_records=50847):
    print(f"Generating {n_records:,} sales transaction records...")
    records = []

    start_date = datetime(2024, 1, 1)
    end_date   = datetime(2024, 12, 31)
    date_range = (end_date - start_date).days

    # Build flat product list
    all_products = []
    cat_weights  = []
    for cat, info in CATEGORIES.items():
        for prod, pmin, pmax in info['products']:
            all_products.append((cat, prod, pmin, pmax))
            cat_weights.append(info['weight'] / len(info['products']))

    cat_weights = np.array(cat_weights)
    cat_weights /= cat_weights.sum()

    customer_pool = [f'CUST{str(i).zfill(5)}' for i in range(1, 8235)]

    for i in range(n_records):
        # Random date with seasonal weighting
        month = np.random.choice(list(MONTHLY_MULT.keys()),
                                  p=np.array(list(MONTHLY_MULT.values())) / sum(MONTHLY_MULT.values()))
        day = np.random.randint(1, 29)
        try:
            txn_date = datetime(2024, month, day)
        except ValueError:
            txn_date = datetime(2024, month, 28)

        # Product
        prod_idx = np.random.choice(len(all_products), p=cat_weights)
        cat, prod_name, pmin, pmax = all_products[prod_idx]

        # Pricing
        unit_price = round(np.random.uniform(pmin, pmax), 2)
        quantity   = int(np.random.choice([1, 1, 1, 2, 2, 3], p=[0.5, 0.2, 0.1, 0.1, 0.06, 0.04]))

        # Discount (higher for Electronics)
        if cat == 'Electronics':
            disc = np.random.beta(2.5, 8) * 0.35
        elif cat == 'Apparel':
            disc = np.random.beta(1.5, 10) * 0.25
        else:
            disc = np.random.beta(1.5, 12) * 0.22
        disc = round(disc, 3)

        region   = np.random.choice(REGIONS, p=REGION_WEIGHTS)
        segment  = np.random.choice(SEGMENTS, p=SEGMENT_WEIGHTS)
        sales_rep = np.random.choice(SALES_REPS)
        customer  = np.random.choice(customer_pool)
        prod_id   = f'PRD{str(prod_idx).zfill(4)}'

        # Introduce 4% data quality issues for realism
        if np.random.random() < 0.016:   # duplicates will be added later
            pass
        if np.random.random() < 0.012:
            unit_price = np.nan  # missing price
        if np.random.random() < 0.008:
            region = np.nan      # missing region

        total_revenue = round(quantity * unit_price * (1 - disc), 2) if not np.isnan(unit_price) else np.nan

        records.append({
            'transaction_id':   f'TXN{str(i + 1).zfill(6)}',
            'transaction_date': txn_date.strftime('%Y-%m-%d'),
            'product_id':       prod_id,
            'product_name':     prod_name,
            'category':         cat,
            'region':           region,
            'sales_rep_id':     sales_rep,
            'customer_id':      customer,
            'customer_segment': segment,
            'quantity':         quantity,
            'unit_price':       unit_price,
            'discount_pct':     disc,
            'total_revenue':    total_revenue,
        })

    df = pd.DataFrame(records)

    # Add ~800 duplicate rows
    dup_indices = np.random.choice(len(df), 800, replace=False)
    duplicates  = df.iloc[dup_indices].copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Raw dataset saved → {OUTPUT_PATH}")
    print(f"   Total rows (incl. duplicates): {len(df):,}")
    print(f"   Columns: {list(df.columns)}")
    return df


if __name__ == '__main__':
    df = generate_dataset()
    print("\nSample rows:")
    print(df.head(3).to_string())
