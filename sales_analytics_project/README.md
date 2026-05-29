# 📊 Sales Performance Analytics Dashboard
### Final Year Internship Project | Data Analytics Domain
**SCET, Sarvajanik University | AI & Data Science | 2025–26**  
**Organization: TechRetail Analytics Pvt. Ltd.**

---

## 🚀 Quick Start (3 Commands)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run full pipeline + launch dashboard
python run_all.py

# 3. Open browser at: http://localhost:8501
```

---

## 📁 Project Structure

```
sales_analytics_project/
├── run_all.py                    ← Master runner (run this!)
├── requirements.txt              ← All Python dependencies
├── README.md                     ← This file
│
├── scripts/
│   ├── 01_generate_dataset.py   ← Generates 50,847 raw sales records
│   ├── 02_data_cleaning.py      ← Cleaning pipeline + quality checks
│   ├── 03_eda_analysis.py       ← EDA → 10 PNG charts saved
│   └── 04_dashboard.py          ← Streamlit interactive dashboard
│
├── data/                         ← Auto-created by scripts
│   ├── sales_raw.csv             ← 51,647 rows (with duplicates/errors)
│   └── sales_clean.csv           ← 50,847 rows (analysis-ready)
│
└── outputs/                      ← Auto-created by scripts
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
```

---

## 🔧 Running Scripts Individually

```bash
# Step 1: Generate raw dataset
python scripts/01_generate_dataset.py

# Step 2: Clean data (removes duplicates, imputes missing values)
python scripts/02_data_cleaning.py

# Step 3: Run EDA (generates all 10 charts)
python scripts/03_eda_analysis.py

# Step 4: Launch dashboard only (skip data generation)
streamlit run scripts/04_dashboard.py
```

### Useful flags:
```bash
# Skip data generation if data already exists
python run_all.py --skip-generate

# Run pipeline only (no dashboard)
python run_all.py --no-dashboard

# Skip dependency check
python run_all.py --no-deps-check
```

---

## 📊 Dashboard Pages

| Page | What You'll See |
|------|----------------|
| 📈 Revenue Overview | Monthly trend (bar+line), Quarterly donut, Key insights |
| 🛍️ Category Analysis | Revenue by category, Discount comparison, Monthly heatmap |
| 🗺️ Regional Performance | Revenue bar chart, Revenue vs. Growth scatter matrix |
| 👥 Customer Intelligence | Segment donut, AOV comparison, Cohort retention heatmap |
| 📦 Products & Discounts | Top-10 products, Discount vs. Revenue scatter, DoW patterns |
| 🗃️ Raw Data | Filtered data table + CSV download |

### Sidebar Filters:
- 📅 Date Range picker
- 🗺️ Region (multi-select)
- 🛍️ Product Category (multi-select)
- 👥 Customer Segment (multi-select)

All charts and KPIs update dynamically based on filters.

---

## 📈 EDA Charts Generated

| Chart | Filename | Description |
|-------|----------|-------------|
| Fig 1 | fig_01_monthly_revenue_trend.png | Bar+Line combo: Revenue & transaction count by month |
| Fig 2 | fig_02_category_analysis.png | Pie chart + Discount bar by category |
| Fig 3 | fig_03_regional_matrix.png | Revenue vs. YoY growth bubble chart |
| Fig 4 | fig_04_customer_segments.png | Nested donut + KPI indexed bar |
| Fig 5 | fig_05_revenue_heatmap.png | Category × Month revenue heatmap |
| Fig 6 | fig_06_discount_impact.png | Discount % vs. revenue scatter + trend |
| Fig 7 | fig_07_quarterly_performance.png | Actual vs. Target grouped bar |
| Fig 8 | fig_08_cohort_retention.png | Retention heatmap H1 2024 |
| Fig 9 | fig_09_top_products.png | Top 10 products horizontal bar |
| Fig 10| fig_10_day_of_week_pattern.png | AOV and count by day of week |

---

## 🗄️ Dataset Description

**Source:** Synthetically generated (realistic retail sales simulation)  
**Records:** ~50,847 clean transactions (51,647 raw with ~800 duplicates + ~1,200 missing values)  
**Period:** January 1, 2024 – December 31, 2024  

| Field | Type | Description |
|-------|------|-------------|
| transaction_id | VARCHAR | Unique transaction ID |
| transaction_date | DATE | Date of sale |
| product_name | VARCHAR | Product name |
| category | VARCHAR | Electronics / Apparel / Home & Living / Food & Bev |
| region | VARCHAR | North / South / East / West / Central |
| customer_segment | VARCHAR | Premium / Standard / Budget |
| quantity | INT | Units sold |
| unit_price | DECIMAL | Price per unit (₹) |
| discount_pct | DECIMAL | Discount fraction (0.00–0.40) |
| total_revenue | DECIMAL | Qty × Price × (1 − Discount) |
| month, quarter, day_of_week | Derived | Time dimension fields |

---

## 🔑 Key Findings

- 💰 **Total Revenue:** ₹24.63 Crore (+14.2% YoY)
- 📅 **Peak Month:** November (Diwali + Year-end promotions)
- 🏆 **Top Category:** Electronics (38.4% revenue share)
- 🗺️ **Top Region:** North (30.1%, +18.3% YoY growth)
- ⚠️ **Concern:** Central region (-2.4% YoY decline)
- 👥 **Premium Customers** (15% base) → 42% of revenue
- 💸 **Discount Sweet Spot:** 8–15% (beyond 25% = diminishing returns)

---

## 🛠️ Tech Stack

| Tool | Version | Use |
|------|---------|-----|
| Python | 3.11+ | Core language |
| Pandas | 2.0+ | Data manipulation |
| NumPy | 1.24+ | Numerical computation |
| Matplotlib | 3.7+ | Static EDA charts |
| Seaborn | 0.12+ | Statistical heatmaps |
| Plotly | 5.15+ | Interactive dashboard charts |
| Streamlit | 1.28+ | Dashboard web app |

---

## 👨‍🎓 Academic Information

- **College:** Sarvajanik College of Engineering & Technology (SCET)
- **University:** Sarvajanik University, Surat
- **Department:** Artificial Intelligence and Data Science
- **Semester:** 8th (Final Year)
- **Internship Duration:** 6–8 Weeks
- **Academic Year:** 2025–26
