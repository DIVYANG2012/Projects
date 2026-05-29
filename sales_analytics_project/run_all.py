"""
=============================================================
 RUN ALL — Master Pipeline Script
 Sales Performance Analytics Dashboard | Internship Project

 Runs all scripts in sequence:
   Step 1: Generate dataset (50,847 rows)
   Step 2: Clean & preprocess data
   Step 3: Run EDA → generate 10 charts
   Step 4: Launch interactive dashboard

 Usage:
   python run_all.py
   python run_all.py --skip-generate   (if data already exists)
   python run_all.py --no-dashboard    (skip dashboard launch)
=============================================================
"""

import subprocess
import sys
import os
import argparse
import time

BASE    = os.path.dirname(__file__)
SCRIPTS = os.path.join(BASE, 'scripts')

STEPS = [
    ('01_generate_dataset.py', 'Generating realistic sales dataset (50,847 rows)'),
    ('02_data_cleaning.py',    'Cleaning data — removing duplicates, filling missing values'),
    ('03_eda_analysis.py',     'Running EDA — generating 10 visualization charts'),
]

def banner(text, char='=', width=62):
    print('\n' + char * width)
    print(f'  {text}')
    print(char * width)

def run_script(script_name, description):
    path = os.path.join(SCRIPTS, script_name)
    print(f'\n▶  {description}')
    print(f'   Script: {script_name}')
    print('   ' + '-' * 50)
    start = time.time()
    result = subprocess.run([sys.executable, path], capture_output=False, text=True)
    elapsed = time.time() - start
    if result.returncode == 0:
        print(f'   ✅ Completed in {elapsed:.1f}s')
        return True
    else:
        print(f'   ❌ Failed with exit code {result.returncode}')
        return False

def check_dependencies():
    banner('CHECKING DEPENDENCIES')
    required = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly', 'streamlit']
    missing  = []
    for pkg in required:
        try:
            __import__(pkg)
            print(f'  ✅ {pkg}')
        except ImportError:
            print(f'  ❌ {pkg}  ← NOT INSTALLED')
            missing.append(pkg)

    if missing:
        print(f'\n⚠️  Missing packages: {", ".join(missing)}')
        print(f'   Run: pip install {" ".join(missing)}')
        ans = input('\n   Auto-install now? (y/n): ').strip().lower()
        if ans == 'y':
            subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing)
        else:
            print('   Exiting. Install dependencies and re-run.')
            sys.exit(1)
    else:
        print('\n  All dependencies satisfied ✅')

def print_project_tree():
    banner('PROJECT STRUCTURE')
    print("""
  sales_analytics_project/
  ├── run_all.py               ← You are here (master runner)
  ├── requirements.txt         ← All dependencies
  ├── README.md                ← Full documentation
  ├── scripts/
  │   ├── 01_generate_dataset.py  ← Generates 50,847 raw transactions
  │   ├── 02_data_cleaning.py     ← Cleaning pipeline (8 quality checks)
  │   ├── 03_eda_analysis.py      ← EDA → 10 chart PNGs
  │   └── 04_dashboard.py         ← Streamlit interactive dashboard
  ├── data/
  │   ├── sales_raw.csv           ← Generated raw data
  │   └── sales_clean.csv         ← Cleaned data (used by dashboard)
  └── outputs/
      ├── charts/
      │   ├── fig_01_monthly_revenue_trend.png
      │   ├── fig_02_category_analysis.png
      │   ├── fig_03_regional_matrix.png
      │   ├── fig_04_customer_segments.png
      │   ├── fig_05_revenue_heatmap.png
      │   ├── fig_06_discount_impact.png
      │   ├── fig_07_quarterly_performance.png
      │   ├── fig_08_cohort_retention.png
      │   ├── fig_09_top_products.png
      │   └── fig_10_day_of_week_pattern.png
      └── data_quality_report.json
""")

def main():
    parser = argparse.ArgumentParser(description='Sales Analytics Project Pipeline')
    parser.add_argument('--skip-generate', action='store_true',
                        help='Skip dataset generation if data already exists')
    parser.add_argument('--no-dashboard', action='store_true',
                        help='Skip launching the Streamlit dashboard')
    parser.add_argument('--no-deps-check', action='store_true',
                        help='Skip dependency check')
    args = parser.parse_args()

    banner('SALES PERFORMANCE ANALYTICS DASHBOARD', '═')
    print("""
  Internship Project | Data Analytics Domain
  SCET, Sarvajanik University | Academic Year 2025-26
  Organization: Buildup Infotech Pvt. Ltd.
""")

    print_project_tree()

    if not args.no_deps_check:
        check_dependencies()

    banner('RUNNING PIPELINE')
    all_ok = True

    for i, (script, desc) in enumerate(STEPS):
        # Skip step 1 if data exists and flag set
        if i == 0 and args.skip_generate:
            raw_path = os.path.join(BASE, 'data', 'sales_raw.csv')
            if os.path.exists(raw_path):
                print(f'\n⏭️  Skipping Step 1 (data already exists at {raw_path})')
                continue

        ok = run_script(script, f'Step {i+1}/{len(STEPS)}: {desc}')
        if not ok:
            print(f'\n❌ Pipeline aborted at Step {i+1}.')
            sys.exit(1)

    # Summary
    banner('PIPELINE COMPLETE ✅')
    out_dir = os.path.join(BASE, 'outputs', 'charts')
    charts  = [f for f in os.listdir(out_dir) if f.endswith('.png')] if os.path.exists(out_dir) else []
    clean   = os.path.join(BASE, 'data', 'sales_clean.csv')
    clean_rows = 0
    if os.path.exists(clean):
        import pandas as pd
        df = pd.read_csv(clean)
        clean_rows = len(df)

    print(f"""
  📁 Data files:
     Raw dataset      : data/sales_raw.csv
     Clean dataset    : data/sales_clean.csv ({clean_rows:,} rows)

  📊 Charts generated: {len(charts)} PNGs in outputs/charts/
  📋 Quality report  : outputs/data_quality_report.json
""")

    if not args.no_dashboard:
        banner('LAUNCHING DASHBOARD 🚀')
        dashboard_path = os.path.join(SCRIPTS, '04_dashboard.py')
        print("""
  Starting Streamlit dashboard...
  Open your browser at: http://localhost:8501

  Dashboard Features:
    📈 Revenue Overview   — Monthly/Quarterly trends
    🛍️ Category Analysis  — Revenue & discount analysis
    🗺️ Regional View      — Performance matrix
    👥 Customer Intel     — Segments & cohort retention
    📦 Products           — Top-10 & discount impact
    🗃️ Raw Data           — Filter & download

  Press Ctrl+C to stop the dashboard.
""")
        os.execv(sys.executable, [sys.executable, '-m', 'streamlit', 'run',
                                   dashboard_path, '--server.port=8501',
                                   '--theme.base=light',
                                   '--theme.primaryColor=#1B3A6B'])

if __name__ == '__main__':
    main()
