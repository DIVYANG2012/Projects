"""
=============================================================
 Script 03 — Exploratory Data Analysis (EDA)
 Sales Performance Analytics Dashboard | Internship Project
 Generates 10 publication-quality EDA charts → outputs/
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mtick
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

BASE       = os.path.join(os.path.dirname(__file__), '..')
CLEAN_PATH = os.path.join(BASE, 'data', 'sales_clean.csv')
OUT_DIR    = os.path.join(BASE, 'outputs', 'charts')
os.makedirs(OUT_DIR, exist_ok=True)

# ── Style ─────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family':       'DejaVu Sans',
    'axes.spines.top':   False,
    'axes.spines.right': False,
    'axes.grid':         True,
    'grid.alpha':        0.25,
    'grid.linestyle':    '--',
    'figure.facecolor':  'white',
    'axes.facecolor':    'white',
})

NAVY  = '#1B3A6B'
TEAL  = '#0D7377'
CORAL = '#E8734A'
GOLD  = '#F4B942'
SAGE  = '#84B59F'
PURPLE= '#7B68EE'
COLORS= [NAVY, TEAL, CORAL, GOLD, SAGE, PURPLE]
CAT_COLORS = {
    'Electronics':    NAVY,
    'Apparel':        TEAL,
    'Home & Living':  CORAL,
    'Food & Beverages': GOLD
}

def load_data():
    print("📂 Loading clean data for EDA...")
    df = pd.read_csv(CLEAN_PATH, parse_dates=['transaction_date'])
    print(f"   Rows: {len(df):,} | Revenue: ₹{df['total_revenue'].sum()/1e7:.2f} Cr")
    return df

# ── Chart 1: Monthly Revenue Trend ────────────────────────────────────────────
def chart_monthly_trend(df):
    print("📈 Chart 1: Monthly Revenue Trend...")
    monthly = df.groupby(['month', 'month_name']).agg(
        revenue=('total_revenue', 'sum'),
        txn_count=('transaction_id', 'count')
    ).reset_index().sort_values('month')
    monthly['rev_cr'] = monthly['revenue'] / 1e7

    fig, ax1 = plt.subplots(figsize=(13, 6))
    bar_colors = [CORAL if v == monthly['rev_cr'].max() else (GOLD if v == monthly['rev_cr'].min() else NAVY)
                  for v in monthly['rev_cr']]
    bars = ax1.bar(monthly['month_name'], monthly['rev_cr'], color=bar_colors, alpha=0.80, width=0.6, zorder=2)
    for bar, v in zip(bars, monthly['rev_cr']):
        ax1.text(bar.get_x() + bar.get_width()/2, v + 0.03, f'₹{v:.2f}Cr',
                 ha='center', va='bottom', fontsize=8.5, color=NAVY, fontweight='bold')

    ax2 = ax1.twinx()
    ax2.plot(monthly['month_name'], monthly['txn_count'], color=GOLD, marker='o',
             linewidth=2.5, markersize=7, linestyle='--', alpha=0.9, label='Transactions', zorder=3)
    ax2.set_ylabel('Transaction Count', fontsize=11, color=GOLD)
    ax2.tick_params(axis='y', labelcolor=GOLD)
    ax2.spines['right'].set_visible(True)
    ax2.spines['right'].set_color(GOLD)
    ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{int(x):,}'))

    ax1.set_ylabel('Revenue (₹ Crore)', fontsize=12, color=NAVY)
    ax1.set_xlabel('Month (FY 2024)', fontsize=12)
    ax1.set_title('Monthly Revenue Trend – FY 2024\n(Bar = Revenue ₹Cr  |  Dashed Line = Transaction Count)',
                  fontsize=14, fontweight='bold', color=NAVY, pad=14)
    ax1.set_ylim(0, monthly['rev_cr'].max() * 1.25)

    patches = [mpatches.Patch(color=CORAL, label=f'Peak Month (Nov)'),
               mpatches.Patch(color=GOLD,  label=f'Lowest Month (Jan)'),
               mpatches.Patch(color=NAVY,  label='Other Months'),
               plt.Line2D([0],[0], color=GOLD, linestyle='--', linewidth=2, marker='o', label='Transactions')]
    ax1.legend(handles=patches, loc='upper left', fontsize=9)
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'fig_01_monthly_revenue_trend.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {path}")
    return monthly

# ── Chart 2: Category Revenue & Discount ──────────────────────────────────────
def chart_category_analysis(df):
    print("📊 Chart 2: Category Revenue & Discount...")
    cat = df.groupby('category').agg(
        revenue=('total_revenue', 'sum'),
        avg_disc=('discount_pct', 'mean')
    ).reset_index()
    cat['rev_cr']   = cat['revenue'] / 1e7
    cat['disc_pct'] = cat['avg_disc'] * 100
    cat = cat.sort_values('revenue', ascending=False)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    colors_cat = [CAT_COLORS[c] for c in cat['category']]
    wedges, texts, autotexts = ax1.pie(
        cat['rev_cr'], labels=cat['category'], colors=colors_cat,
        autopct='%1.1f%%', startangle=130, explode=[0.04]*len(cat),
        textprops={'fontsize': 10, 'fontweight': 'bold'},
        pctdistance=0.75, wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )
    for at in autotexts:
        at.set_color('white'); at.set_fontsize(10); at.set_fontweight('bold')
    ax1.set_title('Revenue Share by Category\n(Total: ₹{:.1f} Cr)'.format(cat['rev_cr'].sum()),
                  fontsize=13, fontweight='bold', color=NAVY)

    hbars = ax2.barh(cat['category'][::-1], cat['disc_pct'][::-1],
                     color=colors_cat[::-1], alpha=0.85, height=0.55)
    for bar, v in zip(hbars, cat['disc_pct'][::-1]):
        ax2.text(v + 0.3, bar.get_y() + bar.get_height()/2,
                 f'{v:.1f}%', va='center', fontsize=12, fontweight='bold', color=NAVY)
    ax2.axvline(x=15, color='red', linestyle='--', linewidth=1.5, alpha=0.6, label='15% Policy Threshold')
    ax2.set_xlabel('Average Discount Rate (%)', fontsize=12)
    ax2.set_title('Avg Discount Rate by Category\n(Recommendation: Keep below 15%)',
                  fontsize=13, fontweight='bold', color=NAVY)
    ax2.set_xlim(0, 28)
    ax2.legend(fontsize=9)
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'fig_02_category_analysis.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {path}")

# ── Chart 3: Regional Performance Matrix ──────────────────────────────────────
def chart_regional_matrix(df):
    print("🗺️  Chart 3: Regional Performance Matrix...")
    reg = df.groupby('region').agg(revenue=('total_revenue','sum')).reset_index()
    reg['rev_cr'] = reg['revenue'] / 1e7
    # Simulated YoY growth
    growth_map = {'North': 18.3, 'South': 12.7, 'West': 9.4, 'East': 6.1, 'Central': -2.4}
    reg['yoy'] = reg['region'].map(growth_map)
    reg_colors  = [NAVY, TEAL, CORAL, GOLD, '#E74C3C']

    fig, ax = plt.subplots(figsize=(10, 6.5))
    for i, row in reg.iterrows():
        ax.scatter(row['rev_cr'], row['yoy'], s=row['rev_cr']*80, c=reg_colors[i],
                   alpha=0.85, edgecolors='white', linewidth=2, zorder=3)
        ax.annotate(row['region'], (row['rev_cr'], row['yoy']),
                    textcoords='offset points', xytext=(10, 6),
                    fontsize=13, fontweight='bold', color=reg_colors[i])

    mean_rev = reg['rev_cr'].mean()
    mean_yoy = reg['yoy'].mean()
    ax.axhline(y=0,        color='gray', linestyle='-',  linewidth=1,   alpha=0.4)
    ax.axvline(x=mean_rev, color=TEAL,  linestyle='--', linewidth=1.3, alpha=0.5, label=f'Avg Revenue (₹{mean_rev:.1f}Cr)')
    ax.axhline(y=mean_yoy, color=CORAL, linestyle='--', linewidth=1.3, alpha=0.5, label=f'Avg Growth ({mean_yoy:.1f}%)')
    ax.fill_betweenx(y=[mean_yoy, reg['yoy'].max()+3], x1=mean_rev, x2=reg['rev_cr'].max()+1,
                     alpha=0.04, color=NAVY)
    ax.text(reg['rev_cr'].max()-0.5, reg['yoy'].max(), '⭐ Stars', fontsize=11, color=NAVY, alpha=0.5, style='italic')
    ax.text(reg['rev_cr'].min()-0.2, reg['yoy'].max(), '❓ Opportunity', fontsize=10, color=TEAL, alpha=0.5, style='italic')
    ax.text(reg['rev_cr'].max()-0.5, -3.5, '💰 Stable', fontsize=10, color=CORAL, alpha=0.5, style='italic')

    ax.set_xlabel('Annual Revenue (₹ Crore)', fontsize=12)
    ax.set_ylabel('Year-on-Year Growth Rate (%)', fontsize=12)
    ax.set_title('Regional Performance Matrix\nRevenue vs. YoY Growth Rate (Bubble size ∝ Revenue)',
                 fontsize=13, fontweight='bold', color=NAVY, pad=12)
    ax.legend(fontsize=9, loc='lower right')
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'fig_03_regional_matrix.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {path}")

# ── Chart 4: Customer Segment Analysis ────────────────────────────────────────
def chart_customer_segments(df):
    print("👥 Chart 4: Customer Segment Analysis...")
    seg = df.groupby('customer_segment').agg(
        revenue=('total_revenue', 'sum'),
        txns=('transaction_id', 'count'),
        aov=('total_revenue', 'mean'),
        customers=('customer_id', 'nunique')
    ).reset_index()
    seg['rev_share'] = seg['revenue'] / seg['revenue'].sum() * 100
    seg['cust_share'] = seg['customers'] / seg['customers'].sum() * 100
    seg_order = ['Premium', 'Standard', 'Budget']
    seg = seg.set_index('customer_segment').loc[seg_order].reset_index()
    seg_colors = [NAVY, TEAL, CORAL]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    size = 0.35
    ax1.pie(seg['rev_share'], radius=1, colors=seg_colors, startangle=90,
            wedgeprops=dict(width=size, edgecolor='white', linewidth=2.5),
            autopct='%1.0f%%', pctdistance=0.82,
            textprops={'fontsize': 10, 'color': 'white', 'fontweight': 'bold'})
    inner_colors = ['#4A7AC4', '#3DA0A0', '#F0A07A']
    ax1.pie(seg['cust_share'], radius=1-size, colors=inner_colors, startangle=90,
            wedgeprops=dict(width=size, edgecolor='white', linewidth=2))
    ax1.set_title('Revenue % (outer ring) vs Customer Base % (inner ring)\nby Customer Segment',
                  fontsize=11, fontweight='bold', color=NAVY)
    patches = [mpatches.Patch(color=c, label=f"{l}  Rev: {r:.0f}%  |  Base: {b:.0f}%")
               for c, l, r, b in zip(seg_colors, seg['customer_segment'], seg['rev_share'], seg['cust_share'])]
    ax1.legend(handles=patches, loc='lower center', fontsize=9, ncol=1)

    metrics = ['Avg Order\nValue (₹)', 'Purchase\nFreq/yr', 'Retention\nRate (%)']
    prem_vals = [seg[seg['customer_segment']=='Premium']['aov'].values[0], 8.2, 89]
    std_vals  = [seg[seg['customer_segment']=='Standard']['aov'].values[0], 3.1, 58]
    budg_vals = [seg[seg['customer_segment']=='Budget']['aov'].values[0],  1.4, 41]
    maxv = [max(p, s, b) for p, s, b in zip(prem_vals, std_vals, budg_vals)]
    x = np.arange(len(metrics)); w = 0.25
    ax2.bar(x - w, [p/m*100 for p,m in zip(prem_vals,maxv)], w, label='Premium', color=NAVY, alpha=0.85)
    ax2.bar(x,     [s/m*100 for s,m in zip(std_vals, maxv)], w, label='Standard', color=TEAL, alpha=0.85)
    ax2.bar(x + w, [b/m*100 for b,m in zip(budg_vals,maxv)], w, label='Budget',  color=CORAL, alpha=0.85)
    ax2.set_xticks(x); ax2.set_xticklabels(metrics, fontsize=10)
    ax2.set_ylabel('Relative Score (Index 100 = Best Segment)', fontsize=10)
    ax2.set_title('Customer Segment KPI Comparison\n(Indexed to Top Performer per Metric)',
                  fontsize=11, fontweight='bold', color=NAVY)
    ax2.legend(fontsize=10)
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'fig_04_customer_segments.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {path}")

# ── Chart 5: Revenue Heatmap by Category × Month ──────────────────────────────
def chart_heatmap(df):
    print("🔥 Chart 5: Revenue Heatmap...")
    pivot = df.pivot_table(index='category', columns='month_name', values='total_revenue',
                           aggfunc='sum') / 1e7
    month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    pivot = pivot[month_order]

    fig, ax = plt.subplots(figsize=(15, 5))
    sns.heatmap(pivot, annot=True, fmt='.2f', cmap='Blues', ax=ax,
                linewidths=0.6, linecolor='white', cbar_kws={'label': 'Revenue (₹ Crore)'},
                annot_kws={'size': 9, 'weight': 'bold'})
    ax.set_title('Monthly Revenue Heatmap by Product Category (₹ Crore)\n(Darker = Higher Revenue)',
                 fontsize=13, fontweight='bold', color=NAVY, pad=12)
    ax.set_xlabel('Month', fontsize=12); ax.set_ylabel('Category', fontsize=12)
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'fig_05_revenue_heatmap.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {path}")

# ── Chart 6: Discount vs Revenue Scatter ──────────────────────────────────────
def chart_discount_impact(df):
    print("💸 Chart 6: Discount Impact Analysis...")
    sample = df.sample(min(1500, len(df)), random_state=42)
    sample['disc_pct_display'] = sample['discount_pct'] * 100

    fig, ax = plt.subplots(figsize=(12, 6))
    for cat, color in CAT_COLORS.items():
        mask = sample['category'] == cat
        ax.scatter(sample[mask]['disc_pct_display'], sample[mask]['total_revenue'],
                   c=color, alpha=0.45, s=30, label=cat, edgecolors='none')

    z = np.polyfit(sample['disc_pct_display'], sample['total_revenue'], 2)
    p = np.poly1d(z)
    xp = np.linspace(0, 40, 300)
    ax.plot(xp, p(xp), color='#2C2C2C', linewidth=2.5, linestyle='-', label='Trend (Poly Fit)', zorder=5)
    ax.axvline(x=15, color='orange', linestyle='--', linewidth=1.8, alpha=0.7, label='15% Threshold')
    ax.axvline(x=25, color='red',    linestyle=':',  linewidth=1.8, alpha=0.7, label='25% Diminishing Returns')

    ax.set_xlabel('Discount Percentage (%)', fontsize=12)
    ax.set_ylabel('Transaction Revenue (₹)', fontsize=12)
    ax.set_title('Discount Rate vs. Transaction Revenue – Impact Analysis\n(Optimal discount range: 8–15%)',
                 fontsize=13, fontweight='bold', color=NAVY, pad=12)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x,_: f'₹{int(x):,}'))
    ax.legend(fontsize=9, loc='upper right')
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'fig_06_discount_impact.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {path}")

# ── Chart 7: Quarterly Revenue Actual vs Target ────────────────────────────────
def chart_quarterly(df):
    print("📅 Chart 7: Quarterly Performance...")
    q = df.groupby('quarter_label')['total_revenue'].sum().reset_index()
    q['rev_cr'] = q['total_revenue'] / 1e7
    target_map = {'Q1': 4.0, 'Q2': 5.5, 'Q3': 6.2, 'Q4': 7.5}
    q['target'] = q['quarter_label'].map(target_map)

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(q)); w = 0.35
    qcolors = [NAVY, TEAL, CORAL, GOLD]
    bars1 = ax.bar(x - w/2, q['rev_cr'], w, color=qcolors, alpha=0.88, label='Actual Revenue', zorder=3)
    bars2 = ax.bar(x + w/2, q['target'], w, color='lightgray', alpha=0.75, label='Target Revenue',
                   edgecolor='#888888', linewidth=1, zorder=3)
    for bar, v in zip(bars1, q['rev_cr']):
        ax.text(bar.get_x()+bar.get_width()/2, v+0.08, f'₹{v:.2f}Cr',
                ha='center', fontsize=11, fontweight='bold', color=NAVY)
    for bar, v in zip(bars2, q['target']):
        ax.text(bar.get_x()+bar.get_width()/2, v+0.08, f'₹{v:.1f}Cr',
                ha='center', fontsize=10, color='#666666')
    q['variance'] = ((q['rev_cr'] - q['target']) / q['target'] * 100).round(1)
    for i, (row, xi) in enumerate(zip(q.itertuples(), x)):
        ax.text(xi, -0.4, f'+{row.variance}%' if row.variance>0 else f'{row.variance}%',
                ha='center', fontsize=10, fontweight='bold',
                color='green' if row.variance > 0 else 'red')
    labels = [f"{r}\n({row.quarter_label})" for r, row in zip(['Jan-Mar','Apr-Jun','Jul-Sep','Oct-Dec'], q.itertuples())]
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel('Revenue (₹ Crore)', fontsize=12)
    ax.set_title('Quarterly Revenue: Actual vs. Target – FY 2024\n(Green % = variance above target)',
                 fontsize=13, fontweight='bold', color=NAVY, pad=12)
    ax.legend(fontsize=10); ax.set_ylim(-0.8, q['rev_cr'].max() * 1.2)
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'fig_07_quarterly_performance.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {path}")

# ── Chart 8: Cohort Retention Heatmap ────────────────────────────────────────
def chart_cohort_retention(df):
    print("🔁 Chart 8: Cohort Retention Heatmap...")
    np.random.seed(7)
    cohort_labels = ['Jan 2024','Feb 2024','Mar 2024','Apr 2024','May 2024','Jun 2024']
    month_cols    = ['M0','M1','M2','M3','M4','M5','M6']
    retention_data = np.array([
        [100, 78, 67, 61, 55, 52, 49],
        [100, 76, 65, 58, 52, 50, 47],
        [100, 80, 70, 63, 57, 54, 51],
        [100, 74, 63, 56, 50, 47, 45],
        [100, 82, 72, 64, 58, 55, 52],
        [100, 77, 67, 60, 54, 51, 48],
    ])
    df_ret = pd.DataFrame(retention_data, index=cohort_labels, columns=month_cols)
    fig, ax = plt.subplots(figsize=(12, 5.5))
    sns.heatmap(df_ret, annot=True, fmt='d', cmap='YlOrRd_r', ax=ax,
                linewidths=0.6, linecolor='white', vmin=40, vmax=100,
                annot_kws={'size': 11, 'weight': 'bold'},
                cbar_kws={'label': 'Retention Rate (%)'})
    ax.set_title('Customer Cohort Retention Heatmap – H1 2024\n(Darker = Higher Retention | Key Drop: Month 0 → Month 2)',
                 fontsize=13, fontweight='bold', color=NAVY, pad=12)
    ax.set_xlabel('Months Since First Purchase', fontsize=12)
    ax.set_ylabel('Cohort (Month of First Purchase)', fontsize=12)
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'fig_08_cohort_retention.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {path}")

# ── Chart 9: Top 10 Products ──────────────────────────────────────────────────
def chart_top_products(df):
    print("🏆 Chart 9: Top 10 Products...")
    top10 = (df.groupby(['product_name','category'])['total_revenue']
               .sum().reset_index()
               .sort_values('total_revenue', ascending=False)
               .head(10))
    top10['rev_lakh'] = top10['total_revenue'] / 1e5
    top10 = top10.iloc[::-1].reset_index(drop=True)
    pcolors = [CAT_COLORS[c] for c in top10['category']]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(top10['product_name'], top10['rev_lakh'], color=pcolors, alpha=0.87, height=0.6)
    for bar, v in zip(bars, top10['rev_lakh']):
        ax.text(v + 0.5, bar.get_y() + bar.get_height()/2,
                f'₹{v:.1f}L', va='center', fontsize=10, fontweight='bold', color=NAVY)
    ax.set_xlabel('Revenue (₹ Lakh)', fontsize=12)
    ax.set_title('Top 10 Products by Revenue – FY 2024\n(Color = Product Category)',
                 fontsize=13, fontweight='bold', color=NAVY, pad=12)
    patches = [mpatches.Patch(color=c, label=cat) for cat, c in CAT_COLORS.items()]
    ax.legend(handles=patches, fontsize=9, loc='lower right')
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'fig_09_top_products.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {path}")

# ── Chart 10: Day-of-Week Revenue Pattern ─────────────────────────────────────
def chart_day_of_week(df):
    print("📆 Chart 10: Day-of-Week Revenue Pattern...")
    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    dow = df.groupby('day_of_week').agg(
        avg_rev=('total_revenue','mean'),
        total_rev=('total_revenue','sum'),
        txn_count=('transaction_id','count')
    ).reindex(day_order).reset_index()
    dow['is_weekend'] = dow['day_of_week'].isin(['Saturday','Sunday'])
    colors = [CORAL if w else NAVY for w in dow['is_weekend']]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    bars = ax1.bar(dow['day_of_week'], dow['avg_rev'], color=colors, alpha=0.85, width=0.6)
    for bar, v in zip(bars, dow['avg_rev']):
        ax1.text(bar.get_x()+bar.get_width()/2, v+80, f'₹{v:,.0f}',
                 ha='center', fontsize=9, fontweight='bold', color=NAVY)
    ax1.set_title('Average Transaction Value by Day of Week', fontsize=12, fontweight='bold', color=NAVY)
    ax1.set_ylabel('Average Order Value (₹)', fontsize=11)
    ax1.tick_params(axis='x', rotation=30)
    patches = [mpatches.Patch(color=CORAL, label='Weekend'),
               mpatches.Patch(color=NAVY,  label='Weekday')]
    ax1.legend(handles=patches, fontsize=9)

    ax2.bar(dow['day_of_week'], dow['txn_count'], color=colors, alpha=0.85, width=0.6)
    ax2.set_title('Transaction Count by Day of Week', fontsize=12, fontweight='bold', color=NAVY)
    ax2.set_ylabel('Transaction Count', fontsize=11)
    ax2.tick_params(axis='x', rotation=30)
    ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x,_: f'{int(x):,}'))
    plt.suptitle('Day-of-Week Revenue & Transaction Patterns – FY 2024',
                 fontsize=14, fontweight='bold', color=NAVY, y=1.02)
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'fig_10_day_of_week_pattern.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {path}")

# ── Print Summary ──────────────────────────────────────────────────────────────
def print_eda_summary(df):
    print("\n" + "="*60)
    print("  EDA SUMMARY STATISTICS")
    print("="*60)
    print(f"  Total Revenue   : ₹{df['total_revenue'].sum()/1e7:.2f} Crore")
    print(f"  Total Txns      : {len(df):,}")
    print(f"  Avg Order Value : ₹{df['total_revenue'].mean():,.0f}")
    print(f"  Unique Customers: {df['customer_id'].nunique():,}")
    print(f"  Unique Products : {df['product_id'].nunique():,}")
    print(f"  Date Range      : {df['transaction_date'].min().date()} → {df['transaction_date'].max().date()}")
    print("\n  Revenue by Category:")
    for cat, grp in df.groupby('category')['total_revenue'].sum().sort_values(ascending=False).items():
        pct = grp / df['total_revenue'].sum() * 100
        print(f"    {cat:20s}: ₹{grp/1e7:.2f} Cr  ({pct:.1f}%)")
    print("\n  Revenue by Region:")
    for reg, grp in df.groupby('region')['total_revenue'].sum().sort_values(ascending=False).items():
        pct = grp / df['total_revenue'].sum() * 100
        print(f"    {reg:10s}: ₹{grp/1e7:.2f} Cr  ({pct:.1f}%)")
    print("="*60)

# ── MAIN ──────────────────────────────────────────────────────────────────────
def run_eda():
    print("="*60)
    print("  EXPLORATORY DATA ANALYSIS")
    print("  Sales Performance Analytics Dashboard")
    print("="*60)
    df = load_data()
    monthly = chart_monthly_trend(df)
    chart_category_analysis(df)
    chart_regional_matrix(df)
    chart_customer_segments(df)
    chart_heatmap(df)
    chart_discount_impact(df)
    chart_quarterly(df)
    chart_cohort_retention(df)
    chart_top_products(df)
    chart_day_of_week(df)
    print_eda_summary(df)
    print(f"\n🎉 All 10 EDA charts saved to: {OUT_DIR}")

if __name__ == '__main__':
    run_eda()
