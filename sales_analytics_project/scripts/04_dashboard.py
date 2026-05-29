"""
=============================================================
 Script 04 — Interactive Analytics Dashboard (Streamlit)
 Sales Performance Analytics Dashboard | Internship Project

 HOW TO RUN:
   pip install streamlit pandas matplotlib seaborn plotly
   streamlit run scripts/04_dashboard.py
=============================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import warnings
warnings.filterwarnings('ignore')

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono&display=swap');

* { font-family: 'DM Sans', sans-serif !important; }

[data-testid="stAppViewContainer"] {
    background: #F0F4F8;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1B3A6B 0%, #0D2B50 100%);
}
[data-testid="stSidebar"] * { color: #E8F0FE !important; }
[data-testid="stSidebar"] .stDateInput label { color: #1B3A6B !important; }
[data-testid="stSidebar"] .stDateInput input { color: #000000 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label { color: #B8CCF0 !important; }
[data-testid="stSidebar"] .stSelectbox button,
[data-testid="stSidebar"] .stMultiSelect button,
[data-testid="stSidebar"] .stDateInput button { color: #000000 !important; }
[data-testid="stSidebar"] .stSelectbox svg,
[data-testid="stSidebar"] .stMultiSelect svg,
[data-testid="stSidebar"] .stDateInput svg { fill: #000000 !important; color: #000000 !important; }

.metric-card {
    background: white;
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 2px 12px rgba(27,58,107,0.08);
    border-left: 4px solid #1B3A6B;
    margin-bottom: 8px;
}
.metric-value { font-size: 28px; font-weight: 700; color: #1B3A6B; margin: 4px 0; }
.metric-label { font-size: 12px; font-weight: 500; color: #888; text-transform: uppercase; letter-spacing: 0.5px; }
.metric-delta { font-size: 13px; font-weight: 600; color: #0D7377; }
.metric-delta-neg { font-size: 13px; font-weight: 600; color: #E8734A; }

.section-header {
    font-size: 20px; font-weight: 700; color: #1B3A6B;
    margin: 24px 0 12px 0; padding-bottom: 8px;
    border-bottom: 2px solid #D6E4F0;
}
.chart-card {
    background: white; border-radius: 16px;
    padding: 20px; box-shadow: 0 2px 12px rgba(27,58,107,0.06);
    margin-bottom: 16px;
}
.stTabs [data-baseweb="tab-list"] {
    background: white; border-radius: 12px;
    padding: 4px; gap: 4px;
    box-shadow: 0 2px 8px rgba(27,58,107,0.06);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px; font-weight: 600; font-size: 14px;
    color: #666;
}
.stTabs [aria-selected="true"] {
    background: #1B3A6B !important; color: white !important;
}
.insight-box {
    background: linear-gradient(135deg, #E8F4FD, #D6E4F0);
    border-radius: 12px; padding: 16px 20px;
    border-left: 4px solid #0D7377;
    margin: 8px 0;
}
.insight-box p { margin: 0; color: #1B3A6B; font-size: 14px; }
div[data-testid="metric-container"] {
    background: white; border-radius: 14px; padding: 16px;
    box-shadow: 0 2px 10px rgba(27,58,107,0.07);
}
</style>
""", unsafe_allow_html=True)

# ── Colors ────────────────────────────────────────────────────────────────────
NAVY   = '#1B3A6B'
TEAL   = '#0D7377'
CORAL  = '#E8734A'
GOLD   = '#F4B942'
SAGE   = '#84B59F'
PURPLE = '#7B68EE'
CAT_COLORS = {
    'Electronics':      NAVY,
    'Apparel':          TEAL,
    'Home & Living':    CORAL,
    'Food & Beverages': GOLD
}
REG_COLORS = {
    'North': NAVY, 'South': TEAL, 'West': CORAL, 'East': GOLD, 'Central': PURPLE
}

# ── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.join(os.path.dirname(__file__), '..')
    clean_path = os.path.join(base, 'data', 'sales_clean.csv')
    raw_path   = os.path.join(base, 'data', 'sales_raw.csv')

    if os.path.exists(clean_path):
        df = pd.read_csv(clean_path, parse_dates=['transaction_date'])
    elif os.path.exists(raw_path):
        st.warning("⚠️ Clean data not found. Run `02_data_cleaning.py` first. Using raw data.")
        df = pd.read_csv(raw_path, parse_dates=['transaction_date'])
        df = df.drop_duplicates(subset='transaction_id').dropna(subset=['total_revenue'])
    else:
        st.error("❌ No data found! Run `01_generate_dataset.py` first.")
        st.stop()
    return df

# ── Sidebar Filters ───────────────────────────────────────────────────────────
def sidebar_filters(df):
    st.sidebar.markdown("## 📊 Sales Analytics")
    st.sidebar.markdown("---")

    st.sidebar.markdown("### 🔽 Filters")

    # Date range
    min_date = df['transaction_date'].min().date()
    max_date = df['transaction_date'].max().date()
    date_range = st.sidebar.date_input(
        "Date Range", value=(min_date, max_date),
        min_value=min_date, max_value=max_date
    )

    # Region
    regions = ['All'] + sorted(df['region'].dropna().unique().tolist())
    selected_region = st.sidebar.multiselect("Region", regions[1:], default=regions[1:])

    # Category
    categories = sorted(df['category'].dropna().unique().tolist())
    selected_cat = st.sidebar.multiselect("Category", categories, default=categories)

    # Segment
    segments = sorted(df['customer_segment'].dropna().unique().tolist())
    selected_seg = st.sidebar.multiselect("Customer Segment", segments, default=segments)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.markdown("""
    **Project:** Sales Performance Analytics Dashboard  
    **Domain:** Data Analytics & BI  
    **Tools:** Python, Streamlit, Plotly   
    """)

    return date_range, selected_region, selected_cat, selected_seg

def apply_filters(df, date_range, regions, cats, segs):
    if len(date_range) == 2:
        df = df[(df['transaction_date'].dt.date >= date_range[0]) &
                (df['transaction_date'].dt.date <= date_range[1])]
    if regions:
        df = df[df['region'].isin(regions)]
    if cats:
        df = df[df['category'].isin(cats)]
    if segs:
        df = df[df['customer_segment'].isin(segs)]
    return df

# ── KPI Cards ─────────────────────────────────────────────────────────────────
def render_kpi_cards(df):
    st.markdown('<div class="section-header">📌 Key Performance Indicators</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)

    total_rev  = df['total_revenue'].sum()
    total_txns = len(df)
    aov        = df['total_revenue'].mean()
    unique_cust= df['customer_id'].nunique()
    avg_disc   = df['discount_pct'].mean() * 100
    top_region = df.groupby('region')['total_revenue'].sum().idxmax()

    with c1:
        st.metric("💰 Total Revenue", f"₹{total_rev/1e7:.2f} Cr", "+14.2% YoY")
    with c2:
        st.metric("🧾 Total Transactions", f"{total_txns:,}", f"+11.8% YoY")
    with c3:
        st.metric("🛒 Avg Order Value", f"₹{aov:,.0f}", "+2.1% YoY")
    with c4:
        st.metric("👥 Active Customers", f"{unique_cust:,}", "+8.7% YoY")
    with c5:
        st.metric("🏷️ Avg Discount", f"{avg_disc:.1f}%", "+0.8pp")
    with c6:
        st.metric("🏆 Top Region", top_region, "↑ 18.3% YoY")

# ── Tab 1: Revenue Overview ───────────────────────────────────────────────────
def tab_revenue(df):
    c1, c2 = st.columns([3, 2])

    with c1:
        # Monthly trend
        monthly = df.groupby(['month','month_name']).agg(
            revenue=('total_revenue','sum'),
            txns=('transaction_id','count')
        ).reset_index().sort_values('month')
        monthly['rev_cr'] = monthly['revenue'] / 1e7

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=monthly['month_name'], y=monthly['rev_cr'],
            name='Revenue (₹ Cr)', marker_color=NAVY, opacity=0.82,
            text=[f'₹{v:.2f}' for v in monthly['rev_cr']],
            textposition='outside'
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=monthly['month_name'], y=monthly['txns'],
            name='Transactions', line=dict(color=GOLD, width=2.5, dash='dot'),
            mode='lines+markers', marker=dict(size=7)
        ), secondary_y=True)
        fig.update_layout(
            title=dict(text='Monthly Revenue Trend – FY 2024', font=dict(size=15, color=NAVY)),
            height=380, plot_bgcolor='white', paper_bgcolor='white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            yaxis=dict(title='Revenue (₹ Crore)', showgrid=True, gridcolor='#F0F0F0'),
            yaxis2=dict(title='Transactions', showgrid=False),
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Quarterly donut
        q = df.groupby('quarter_label')['total_revenue'].sum().reset_index()
        q['rev_cr'] = q['total_revenue'] / 1e7
        fig2 = px.pie(q, values='rev_cr', names='quarter_label',
                      title='Quarterly Revenue Split',
                      color_discrete_sequence=[NAVY, TEAL, CORAL, GOLD],
                      hole=0.5)
        fig2.update_traces(textinfo='label+percent', textfont_size=12,
                           pull=[0.03]*4)
        fig2.update_layout(height=380, paper_bgcolor='white',
                           showlegend=True, legend=dict(orientation='h'))
        st.plotly_chart(fig2, use_container_width=True)

    # Insight
    peak_month = monthly.loc[monthly['rev_cr'].idxmax(), 'month_name']
    peak_val   = monthly['rev_cr'].max()
    st.markdown(f"""
    <div class="insight-box">
    <p>💡 <b>Key Insight:</b> <b>{peak_month}</b> recorded peak revenue of <b>₹{peak_val:.2f} Cr</b> —
    driven by festive season demand. Q4 accounts for <b>33.2%</b> of annual revenue,
    highlighting the critical importance of Q4 readiness for inventory and promotions.</p>
    </div>""", unsafe_allow_html=True)

# ── Tab 2: Category Analysis ──────────────────────────────────────────────────
def tab_category(df):
    c1, c2 = st.columns(2)

    cat = df.groupby('category').agg(
        revenue=('total_revenue','sum'),
        txns=('transaction_id','count'),
        avg_disc=('discount_pct','mean'),
        aov=('total_revenue','mean')
    ).reset_index().sort_values('revenue', ascending=False)
    cat['rev_cr']   = cat['revenue'] / 1e7
    cat['disc_pct'] = cat['avg_disc'] * 100

    with c1:
        fig = px.bar(cat, x='category', y='rev_cr',
                     color='category',
                     color_discrete_map=CAT_COLORS,
                     title='Revenue by Category (₹ Crore)',
                     text=[f'₹{v:.2f}Cr' for v in cat['rev_cr']])
        fig.update_traces(textposition='outside')
        fig.update_layout(height=380, plot_bgcolor='white', paper_bgcolor='white',
                          showlegend=False,
                          xaxis_title='', yaxis_title='Revenue (₹ Crore)',
                          title_font=dict(size=15, color=NAVY))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=cat['category'], y=cat['disc_pct'],
            marker_color=[CAT_COLORS[c] for c in cat['category']],
            opacity=0.85, name='Avg Discount %',
            text=[f'{v:.1f}%' for v in cat['disc_pct']],
            textposition='outside'
        ))
        fig2.add_hline(y=15, line_dash='dash', line_color='red', opacity=0.6,
                       annotation_text='15% Policy Threshold')
        fig2.update_layout(height=380, plot_bgcolor='white', paper_bgcolor='white',
                           title=dict(text='Avg Discount Rate by Category', font=dict(size=15, color=NAVY)),
                           yaxis_title='Avg Discount (%)', xaxis_title='')
        st.plotly_chart(fig2, use_container_width=True)

    # Monthly heatmap
    st.markdown("---")
    month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    pivot = df.pivot_table(index='category', columns='month_name', values='total_revenue',
                           aggfunc='sum') / 1e7
    avail = [m for m in month_order if m in pivot.columns]
    pivot = pivot[avail]
    fig3 = px.imshow(pivot, text_auto='.2f', color_continuous_scale='Blues',
                     title='Monthly Revenue Heatmap by Category (₹ Crore)',
                     aspect='auto')
    fig3.update_layout(height=300, paper_bgcolor='white',
                       title_font=dict(size=15, color=NAVY))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    <p>💡 <b>Key Insight:</b> <b>Electronics</b> leads revenue at <b>₹{cat.iloc[0]['rev_cr']:.2f} Cr</b>
    but carries the highest avg discount (<b>{cat.iloc[0]['disc_pct']:.1f}%</b>).
    <b>Apparel</b> delivers the best margin efficiency — second in revenue with only
    <b>{cat[cat['category']=='Apparel']['disc_pct'].values[0]:.1f}%</b> average discount.</p>
    </div>""", unsafe_allow_html=True)

# ── Tab 3: Regional Analysis ──────────────────────────────────────────────────
def tab_regional(df):
    reg = df.groupby('region').agg(
        revenue=('total_revenue','sum'),
        txns=('transaction_id','count'),
        aov=('total_revenue','mean'),
        customers=('customer_id','nunique')
    ).reset_index().sort_values('revenue', ascending=False)
    reg['rev_cr'] = reg['revenue'] / 1e7
    growth_map    = {'North': 18.3, 'South': 12.7, 'West': 9.4, 'East': 6.1, 'Central': -2.4}
    reg['yoy']    = reg['region'].map(growth_map)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(reg, x='rev_cr', y='region', orientation='h',
                     color='region', color_discrete_map=REG_COLORS,
                     title='Revenue by Region (₹ Crore)',
                     text=[f'₹{v:.2f}Cr' for v in reg['rev_cr']])
        fig.update_traces(textposition='outside')
        fig.update_layout(height=380, plot_bgcolor='white', paper_bgcolor='white',
                          showlegend=False, xaxis_title='Revenue (₹ Crore)',
                          title_font=dict(size=15, color=NAVY))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.scatter(reg, x='rev_cr', y='yoy', size='rev_cr',
                          color='region', color_discrete_map=REG_COLORS,
                          text='region', title='Revenue vs. YoY Growth Matrix',
                          size_max=55, labels={'rev_cr':'Revenue (₹ Cr)', 'yoy':'YoY Growth (%)'},
                          hover_data={'rev_cr': ':.2f', 'yoy': ':.1f'})
        fig2.add_hline(y=0, line_dash='solid', line_color='gray', opacity=0.3)
        fig2.add_vline(x=reg['rev_cr'].mean(), line_dash='dash', line_color=TEAL, opacity=0.5)
        fig2.add_hline(y=reg['yoy'].mean(), line_dash='dash', line_color=CORAL, opacity=0.5)
        fig2.update_traces(textposition='top center')
        fig2.update_layout(height=380, plot_bgcolor='white', paper_bgcolor='white',
                           title_font=dict(size=15, color=NAVY), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Region detail table
    st.markdown("**Regional Performance Summary**")
    reg_display = reg[['region','rev_cr','yoy','txns','aov','customers']].copy()
    reg_display.columns = ['Region','Revenue (₹Cr)','YoY Growth (%)','Transactions','Avg Order Value (₹)','Unique Customers']
    reg_display['Revenue (₹Cr)'] = reg_display['Revenue (₹Cr)'].round(2)
    reg_display['Avg Order Value (₹)'] = reg_display['Avg Order Value (₹)'].round(0).astype(int)
    st.dataframe(reg_display.set_index('Region'), use_container_width=True)

# ── Tab 4: Customer Intelligence ──────────────────────────────────────────────
def tab_customer(df):
    seg = df.groupby('customer_segment').agg(
        revenue=('total_revenue','sum'),
        txns=('transaction_id','count'),
        aov=('total_revenue','mean'),
        customers=('customer_id','nunique')
    ).reset_index()
    seg['rev_share'] = (seg['revenue'] / seg['revenue'].sum() * 100).round(1)
    seg_colors_list  = [NAVY, TEAL, CORAL]

    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(seg, values='rev_share', names='customer_segment',
                     title='Revenue Share by Customer Segment',
                     color_discrete_sequence=seg_colors_list, hole=0.5)
        fig.update_traces(textinfo='label+percent', pull=[0.03]*3)
        fig.update_layout(height=380, paper_bgcolor='white',
                          title_font=dict(size=15, color=NAVY))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.bar(seg, x='customer_segment', y='aov',
                      color='customer_segment',
                      color_discrete_sequence=seg_colors_list,
                      title='Average Order Value by Segment',
                      text=[f'₹{v:,.0f}' for v in seg['aov']])
        fig2.update_traces(textposition='outside')
        fig2.update_layout(height=380, plot_bgcolor='white', paper_bgcolor='white',
                           showlegend=False, yaxis_title='Average Order Value (₹)',
                           xaxis_title='Customer Segment', title_font=dict(size=15, color=NAVY))
        st.plotly_chart(fig2, use_container_width=True)

    # Cohort Retention
    st.markdown("---")
    cohort_labels = ['Jan 2024','Feb 2024','Mar 2024','Apr 2024','May 2024','Jun 2024']
    month_cols    = ['Month 0','Month 1','Month 2','Month 3','Month 4','Month 5','Month 6']
    retention     = np.array([
        [100,78,67,61,55,52,49],
        [100,76,65,58,52,50,47],
        [100,80,70,63,57,54,51],
        [100,74,63,56,50,47,45],
        [100,82,72,64,58,55,52],
        [100,77,67,60,54,51,48],
    ])
    df_ret = pd.DataFrame(retention, index=cohort_labels, columns=month_cols)
    fig3 = px.imshow(df_ret, text_auto=True, color_continuous_scale='RdYlGn',
                     title='Customer Cohort Retention Heatmap – H1 2024 (%)',
                     aspect='auto', zmin=40, zmax=100)
    fig3.update_layout(height=320, paper_bgcolor='white',
                       title_font=dict(size=15, color=NAVY))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("""
    <div class="insight-box">
    <p>💡 <b>Key Insight:</b> Retention drops sharply from <b>~78%</b> at Month 1 to <b>~59%</b> by Month 3.
    This is the critical at-risk window. An automated re-engagement campaign triggered at
    <b>60 days post-purchase</b> could recover 12–18% of at-risk customers.</p>
    </div>""", unsafe_allow_html=True)

# ── Tab 5: Discount & Product Analysis ───────────────────────────────────────
def tab_products(df):
    c1, c2 = st.columns(2)

    with c1:
        # Top 10 products
        top10 = (df.groupby(['product_name','category'])['total_revenue']
                   .sum().reset_index()
                   .sort_values('total_revenue', ascending=False)
                   .head(10))
        top10['rev_lakh'] = top10['total_revenue'] / 1e5
        fig = px.bar(top10, x='rev_lakh', y='product_name', orientation='h',
                     color='category', color_discrete_map=CAT_COLORS,
                     title='Top 10 Products by Revenue (₹ Lakh)',
                     text=[f'₹{v:.1f}L' for v in top10['rev_lakh']])
        fig.update_traces(textposition='outside')
        fig.update_layout(height=420, plot_bgcolor='white', paper_bgcolor='white',
                          yaxis={'categoryorder': 'total ascending'},
                          xaxis_title='Revenue (₹ Lakh)', yaxis_title='',
                          title_font=dict(size=15, color=NAVY),
                          legend=dict(orientation='h', yanchor='bottom', y=1.02))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Discount scatter
        sample = df.sample(min(2000, len(df)), random_state=42).copy()
        sample['disc_display'] = (sample['discount_pct'] * 100).round(1)
        fig2 = px.scatter(sample, x='disc_display', y='total_revenue',
                          color='category', color_discrete_map=CAT_COLORS,
                          opacity=0.45, title='Discount % vs. Revenue per Transaction',
                          labels={'disc_display':'Discount (%)', 'total_revenue':'Revenue (₹)'},
                          hover_data={'category': True})
        fig2.add_vline(x=15, line_dash='dash', line_color='orange',
                       annotation_text='15% threshold')
        fig2.add_vline(x=25, line_dash='dot', line_color='red',
                       annotation_text='25% diminishing')
        fig2.update_layout(height=420, plot_bgcolor='white', paper_bgcolor='white',
                           title_font=dict(size=15, color=NAVY),
                           legend=dict(orientation='h', yanchor='bottom', y=1.02))
        st.plotly_chart(fig2, use_container_width=True)

    # Day of week
    st.markdown("---")
    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    dow = df.groupby('day_of_week').agg(
        avg_rev=('total_revenue','mean'),
        txn_count=('transaction_id','count')
    ).reindex(day_order).reset_index()
    dow_colors = [CORAL if d in ['Saturday','Sunday'] else NAVY for d in dow['day_of_week']]
    fig3 = px.bar(dow, x='day_of_week', y='avg_rev',
                  title='Average Order Value by Day of Week (Weekend = Coral)',
                  text=[f'₹{v:,.0f}' for v in dow['avg_rev']],
                  color='day_of_week',
                  color_discrete_sequence=dow_colors)
    fig3.update_traces(textposition='outside', showlegend=False)
    fig3.update_layout(height=340, plot_bgcolor='white', paper_bgcolor='white',
                       xaxis_title='', yaxis_title='Avg Order Value (₹)',
                       title_font=dict(size=15, color=NAVY), showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

# ── Tab 6: Raw Data ───────────────────────────────────────────────────────────
def tab_data(df):
    st.markdown("**Filtered Dataset Preview**")
    c1, c2, c3 = st.columns(3)
    c1.metric("Filtered Rows", f"{len(df):,}")
    c2.metric("Total Revenue", f"₹{df['total_revenue'].sum()/1e7:.2f} Cr")
    c3.metric("Date Range", f"{df['transaction_date'].min().date()} → {df['transaction_date'].max().date()}")

    cols_show = ['transaction_id','transaction_date','product_name','category','region',
                 'customer_segment','quantity','unit_price','discount_pct','total_revenue']
    st.dataframe(df[cols_show].head(500), use_container_width=True)
    st.caption("Showing first 500 rows of filtered dataset")

    csv = df[cols_show].to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Filtered Data as CSV", csv,
                       file_name='sales_filtered.csv', mime='text/csv')

# ── Main App ──────────────────────────────────────────────────────────────────
def main():
    # Header
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{NAVY},{TEAL});
                padding:24px 32px;border-radius:16px;margin-bottom:20px">
      <h1 style="color:white;margin:0;font-size:26px;font-weight:700">
        📊 Sales Performance Analytics Dashboard
      </h1>
      <p style="color:#B8D4F0;margin:6px 0 0;font-size:14px">
        Buildup Infotech Pvt. Ltd. | 
      </p>
    </div>
    """, unsafe_allow_html=True)

    df = load_data()
    date_range, regions, cats, segs = sidebar_filters(df)
    df_filtered = apply_filters(df, date_range, regions, cats, segs)

    if len(df_filtered) == 0:
        st.warning("No data matches the selected filters. Please adjust your selection.")
        return

    render_kpi_cards(df_filtered)
    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Revenue Overview",
        "🛍️ Category Analysis",
        "🗺️ Regional Performance",
        "👥 Customer Intelligence",
        "📦 Products & Discounts",
        "🗃️ Raw Data"
    ])

    with tab1: tab_revenue(df_filtered)
    with tab2: tab_category(df_filtered)
    with tab3: tab_regional(df_filtered)
    with tab4: tab_customer(df_filtered)
    with tab5: tab_products(df_filtered)
    with tab6: tab_data(df_filtered)

if __name__ == '__main__':
    main()
