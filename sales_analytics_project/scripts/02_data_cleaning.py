"""
=============================================================
 Script 02 — Data Cleaning Pipeline
 Sales Performance Analytics Dashboard | Internship Project
 Cleans raw dataset → produces analysis-ready CSV
=============================================================
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

BASE = os.path.join(os.path.dirname(__file__), '..')
RAW_PATH   = os.path.join(BASE, 'data', 'sales_raw.csv')
CLEAN_PATH = os.path.join(BASE, 'data', 'sales_clean.csv')
REPORT_PATH= os.path.join(BASE, 'outputs', 'data_quality_report.json')

# ─────────────────────────────────────────────────────────────────────────────
def load_data():
    print("📂 Loading raw data...")
    df = pd.read_csv(RAW_PATH, parse_dates=['transaction_date'])
    print(f"   Loaded {len(df):,} rows, {df.shape[1]} columns")
    return df

def profile_data(df):
    """Run initial data quality profile."""
    report = {
        'run_timestamp': datetime.now().isoformat(),
        'total_rows_raw': len(df),
        'total_columns': df.shape[1],
        'duplicates': int(df.duplicated(subset='transaction_id').sum()),
        'missing_values': df.isnull().sum().to_dict(),
        'dtypes': df.dtypes.astype(str).to_dict(),
    }
    print(f"\n📊 Data Quality Profile:")
    print(f"   Total rows        : {report['total_rows_raw']:,}")
    print(f"   Duplicate trans_id: {report['duplicates']:,}")
    print(f"   Missing values    :")
    for col, cnt in report['missing_values'].items():
        if cnt > 0:
            print(f"     {col:25s}: {cnt:,}")
    return report

def remove_duplicates(df, report):
    before = len(df)
    df = df.drop_duplicates(subset='transaction_id', keep='first')
    removed = before - len(df)
    report['duplicates_removed'] = removed
    print(f"\n🔄 Duplicates removed: {removed:,}")
    return df

def handle_missing_values(df, report):
    print("\n🔧 Handling missing values...")
    # unit_price → group median by category
    missing_price = df['unit_price'].isnull().sum()
    df['unit_price'] = df.groupby('category')['unit_price'].transform(
        lambda x: x.fillna(x.median())
    )
    print(f"   unit_price imputed (category median): {missing_price:,} rows")

    # region → mode per sales_rep_id
    missing_region = df['region'].isnull().sum()
    df['region'] = df.groupby('sales_rep_id')['region'].transform(
        lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else 'Unknown')
    )
    print(f"   region imputed (sales rep mode)     : {missing_region:,} rows")

    report['missing_imputed'] = {
        'unit_price': int(missing_price),
        'region':     int(missing_region)
    }
    return df

def remove_outliers(df, report):
    print("\n🔍 Detecting and removing outliers...")
    before = len(df)

    # Remove invalid discounts (>40%)
    df = df[df['discount_pct'].between(0, 0.40)]
    # Remove zero/negative quantities
    df = df[df['quantity'] > 0]
    # Remove zero unit prices
    df = df[df['unit_price'] > 0]

    removed = before - len(df)
    report['outliers_removed'] = removed
    print(f"   Outlier rows removed: {removed:,}")
    return df

def add_derived_fields(df):
    print("\n✨ Adding derived fields...")
    df['total_revenue'] = (df['quantity'] * df['unit_price'] * (1 - df['discount_pct'])).round(2)
    df['month']         = df['transaction_date'].dt.month
    df['month_name']    = df['transaction_date'].dt.strftime('%b')
    df['quarter']       = df['transaction_date'].dt.quarter
    df['quarter_label'] = 'Q' + df['quarter'].astype(str)
    df['day_of_week']   = df['transaction_date'].dt.day_name()
    df['week_number']   = df['transaction_date'].dt.isocalendar().week.astype(int)
    df['is_weekend']    = df['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)
    df['year']          = df['transaction_date'].dt.year

    # RFM Score (simplified)
    seg_map = {'Premium': 3, 'Standard': 2, 'Budget': 1}
    df['segment_score'] = df['customer_segment'].map(seg_map).fillna(1)
    print(f"   Derived fields added: {['total_revenue','month','quarter','day_of_week','week_number','is_weekend','quarter_label']}")
    return df

def validate_dataset(df):
    print("\n✅ Running validation checks...")
    checks = {
        'no_duplicate_ids':      df['transaction_id'].nunique() == len(df),
        'no_missing_unit_price': df['unit_price'].isnull().sum() == 0,
        'no_missing_region':     df['region'].isnull().sum() == 0,
        'discount_in_range':     df['discount_pct'].between(0, 0.40).all(),
        'quantity_positive':     (df['quantity'] > 0).all(),
        'revenue_positive':      (df['total_revenue'] > 0).all(),
        'date_in_2024':          df['transaction_date'].dt.year.eq(2024).all(),
        'all_categories_valid':  df['category'].isin(['Electronics','Apparel','Home & Living','Food & Beverages']).all(),
    }
    all_passed = all(checks.values())
    for check, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}  {check}")
    return all_passed, checks

def save_outputs(df, report, checks):
    os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

    df.to_csv(CLEAN_PATH, index=False)
    print(f"\n💾 Clean dataset saved → {CLEAN_PATH}")
    print(f"   Final rows: {len(df):,}")

    report['final_rows']    = len(df)
    report['validation']    = {k: bool(v) for k, v in checks.items()}
    report['total_revenue'] = round(df['total_revenue'].sum(), 2)
    report['date_range']    = f"{df['transaction_date'].min().date()} to {df['transaction_date'].max().date()}"

    with open(REPORT_PATH, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print(f"📋 Quality report saved → {REPORT_PATH}")

def run_pipeline():
    print("=" * 60)
    print("  DATA CLEANING PIPELINE")
    print("  Sales Performance Analytics Dashboard")
    print("=" * 60)

    df     = load_data()
    report = profile_data(df)
    df     = remove_duplicates(df, report)
    df     = handle_missing_values(df, report)
    df     = remove_outliers(df, report)
    df     = add_derived_fields(df)
    passed, checks = validate_dataset(df)
    save_outputs(df, report, checks)

    print("\n" + "=" * 60)
    if passed:
        print("  🎉 PIPELINE COMPLETE — All validation checks passed!")
    else:
        print("  ⚠️  PIPELINE COMPLETE — Some checks failed. Review report.")
    print("=" * 60)
    return df

if __name__ == '__main__':
    df = run_pipeline()
    print(f"\nPreview:\n{df.head(3).to_string()}")
