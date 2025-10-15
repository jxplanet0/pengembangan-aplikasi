import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Online Retail",
    page_icon="🛒",
    layout="wide"
)

# Custom CSS untuk styling yang lebih baik
st.markdown("""
    <style>
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .kpi-description {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
    .metric-help {
        font-size: 0.85em;
        color: #6c757d;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Fungsi untuk load dataset
@st.cache_data
def load_data():
    """
    Load Online Retail Dataset dari file lokal (online-retail-dataset.csv)
    Dataset: Transaksi retail online UK 2010-2011
    """
    try:
        file_path = "online-retail-dataset.csv"
        st.info(f"📂 Membaca data dari file lokal: {file_path}")
        
        df = pd.read_csv(file_path, encoding='ISO-8859-1', parse_dates=['InvoiceDate']) 
        
        # Data cleaning
        df = df.dropna(subset=['CustomerID']) 
        df = df[df['Quantity'] > 0]
        df = df[df['UnitPrice'] > 0]
        
        # Feature engineering
        df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
        df['Year'] = df['InvoiceDate'].dt.year
        df['Month'] = df['InvoiceDate'].dt.month
        df['MonthName'] = df['InvoiceDate'].dt.strftime('%B')
        df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()
        df['Country'] = df['Country'].str.strip()
        
        # Kategorisasi produk
        def categorize_product(desc):
            if pd.isna(desc):
                return 'Other'
            desc = str(desc).upper()
            if any(word in desc for word in ['BAG', 'BASKET', 'BOX', 'CASE']):
                return 'Storage & Containers'
            elif any(word in desc for word in ['LIGHT', 'CANDLE', 'LAMP']):
                return 'Lighting'
            elif any(word in desc for word in ['SET', 'KIT', 'HOLDER']):
                return 'Sets & Accessories'
            elif any(word in desc for word in ['CARD', 'PAPER', 'WRAP', 'GIFT']):
                return 'Stationery & Gifts'
            elif any(word in desc for word in ['DECOR', 'DECORATION', 'ORNAMENT', 'BUNTING']):
                return 'Decorations'
            else:
                return 'Other'
        
        df['Category'] = df['Description'].apply(categorize_product)
        
        return df
    
    except FileNotFoundError:
        st.error(f"❌ Error: File '{file_path}' tidak ditemukan. Pastikan Anda sudah mengunduh data dan meletakkannya di direktori yang sama dengan aplikasi Streamlit.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return None

# Load data dengan progress bar
with st.spinner('⏳ Loading Online Retail Dataset...'):
    df = load_data()

if df is None:
    st.stop()

# Header dengan styling lebih baik
st.title("🛒 Dashboard Analisis Online Retail")
st.markdown(f"""
<div style='background-color: #2424F0; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
    <p style='margin: 0;'><b>📊 Dataset:</b> UCI Online Retail Dataset</p>
    <p style='margin: 5px 0 0 0;'><b>📅 Periode:</b> {df['InvoiceDate'].min().strftime('%d %B %Y')} - {df['InvoiceDate'].max().strftime('%d %B %Y')}</p>
    <p style='margin: 5px 0 0 0;'><b>📍 Negara:</b> {df['Country'].nunique()} negara | <b>👥 Pelanggan:</b> {df['CustomerID'].nunique():,} pelanggan unik</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Filter
st.sidebar.header("🔍 Filter Data")

# Filter Tahun
year_options = sorted(df['Year'].unique())
selected_year = st.sidebar.selectbox(
    "Pilih Tahun:",
    options=year_options,
    index=len(year_options)-1
)

# Filter Negara (top 10 countries by revenue)
top_countries = df.groupby('Country')['TotalPrice'].sum().nlargest(10).index.tolist()
selected_countries = st.sidebar.multiselect(
    "Pilih Negara (Top 10):",
    options=top_countries,
    default=top_countries[:5]
)

# Filter Kategori
selected_categories = st.sidebar.multiselect(
    "Pilih Kategori Produk:",
    options=sorted(df['Category'].unique()),
    default=sorted(df['Category'].unique())
)

# Apply filters
df_filtered = df[
    (df['Year'] == selected_year) & 
    (df['Country'].isin(selected_countries)) &
    (df['Category'].isin(selected_categories))
]

st.sidebar.markdown("---")
st.sidebar.markdown(f"📊 **Total Records Terfilter:** {len(df_filtered):,}")
st.sidebar.markdown(f"📦 **Total Dataset:** {len(df):,}")

# KPI Section dengan Penjelasan
st.header("📊 Key Performance Indicators (KPI)")

# Penjelasan KPI di atas
with st.expander("ℹ️ Penjelasan Key Performance Indicators", expanded=False):
    st.markdown("""
    <div class='kpi-description'>
        <h4>📌 Apa itu KPI?</h4>
        <p><b>Key Performance Indicators (KPI)</b> adalah metrik kunci yang digunakan untuk mengukur kinerja bisnis. 
        KPI membantu manajemen memahami performa toko dan membuat keputusan strategis.</p>
        
        <h4>📊 KPI yang Ditampilkan:</h4>
        
        <p><b>💰 Total Revenue (Pendapatan Total):</b></p>
        <ul>
            <li>Mengukur total pendapatan dari penjualan dalam periode yang dipilih</li>
            <li><b>Delta YoY</b>: Perbandingan dengan tahun sebelumnya (Year-over-Year growth)</li>
            <li><b>Interpretasi</b>: Semakin tinggi revenue dan pertumbuhan YoY positif = performa baik</li>
        </ul>
        
        <p><b>📦 Total Orders (Total Pesanan):</b></p>
        <ul>
            <li>Jumlah invoice/transaksi unik yang terjadi</li>
            <li><b>Delta</b>: Menampilkan total item yang terjual</li>
            <li><b>Interpretasi</b>: Indikator aktivitas bisnis - banyak pesanan = bisnis aktif</li>
        </ul>
        
        <p><b>👥 Unique Customers (Pelanggan Unik):</b></p>
        <ul>
            <li>Jumlah pelanggan berbeda yang melakukan pembelian</li>
            <li><b>Delta</b>: Average Revenue per Customer (ARPC) - rata-rata pengeluaran per pelanggan</li>
            <li><b>Interpretasi</b>: ARPC tinggi = pelanggan bernilai tinggi (high-value customers)</li>
        </ul>
        
        <p><b>💳 Average Order Value (AOV - Nilai Rata-rata Pesanan):</b></p>
        <ul>
            <li>Rata-rata nilai transaksi per pesanan (Revenue ÷ Total Orders)</li>
            <li><b>Delta</b>: Indikator "Good" (>£300) atau "Low" (<£300)</li>
            <li><b>Interpretasi</b>: AOV tinggi = strategi upselling/cross-selling berhasil</li>
        </ul>
        
        <p><b>🎯 Mengapa KPI Penting?</b></p>
        <ul>
            <li><b>Monitoring:</b> Memantau kesehatan bisnis secara real-time</li>
            <li><b>Benchmarking:</b> Membandingkan performa antar periode</li>
            <li><b>Decision Making:</b> Dasar pengambilan keputusan strategis (promosi, inventory, marketing)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Kalkulasi KPI
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = df_filtered['TotalPrice'].sum()
    # Hitung perubahan YoY
    prev_year = selected_year - 1
    if prev_year in df['Year'].values:
        prev_revenue = df[(df['Year'] == prev_year) & (df['Country'].isin(selected_countries))]['TotalPrice'].sum()
        delta = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
        delta_text = f"{delta:.1f}% YoY"
    else:
        delta_text = "No comparison"
    
    st.metric(
        label="💰 Total Revenue",
        value=f"£{total_revenue:,.0f}",
        delta=delta_text,
        help="Total pendapatan dari semua transaksi. Delta menunjukkan pertumbuhan Year-over-Year (YoY)"
    )
    st.markdown("<p class='metric-help'>📈 Pendapatan dari semua transaksi</p>", unsafe_allow_html=True)

with col2:
    total_orders = df_filtered['InvoiceNo'].nunique()
    total_items = len(df_filtered)
    st.metric(
        label="📦 Total Orders",
        value=f"{total_orders:,}",
        delta=f"{total_items:,} items",
        help="Jumlah invoice/transaksi unik. Delta menunjukkan total item yang terjual"
    )
    st.markdown("<p class='metric-help'>🧾 Jumlah transaksi unik</p>", unsafe_allow_html=True)

with col3:
    total_customers = df_filtered['CustomerID'].nunique()
    arpc = total_revenue/total_customers if total_customers > 0 else 0
    st.metric(
        label="👥 Unique Customers",
        value=f"{total_customers:,}",
        delta=f"£{arpc:.0f} ARPC" if total_customers > 0 else "N/A",
        help="Jumlah pelanggan unik. ARPC = Average Revenue Per Customer (rata-rata belanja per pelanggan)"
    )
    st.markdown("<p class='metric-help'>👤 Pelanggan berbeda yang membeli</p>", unsafe_allow_html=True)

with col4:
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    aov_status = "Good 👍" if avg_order_value > 300 else "Low 📉"
    st.metric(
        label="💳 Avg Order Value (AOV)",
        value=f"£{avg_order_value:,.2f}",
        delta=aov_status,
        help="Rata-rata nilai per transaksi (Revenue ÷ Orders). AOV >£300 dianggap baik untuk retail ini"
    )
    st.markdown("<p class='metric-help'>💵 Nilai rata-rata per pesanan</p>", unsafe_allow_html=True)

st.markdown("---")

# Grafik 1: Tren Revenue Bulanan dengan lebih banyak insight
st.header("📈 Tren Revenue Bulanan")

col_chart, col_insight = st.columns([3, 1])

with col_chart:
    df_monthly = df_filtered.groupby(['Month', 'MonthName']).agg({
        'TotalPrice': 'sum',
        'InvoiceNo': 'nunique',
        'CustomerID': 'nunique'
    }).reset_index()
    
    df_monthly = df_monthly.sort_values('Month')
    
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(
        x=df_monthly['MonthName'],
        y=df_monthly['TotalPrice'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=12, color='#A23B72', line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor='rgba(46, 134, 171, 0.1)',
        hovertemplate='<b>%{x}</b><br>Revenue: £%{y:,.0f}<br><extra></extra>'
    ))
    
    fig1.update_layout(
        xaxis_title="Bulan",
        yaxis_title="Total Revenue (£)",
        hovermode='x unified',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    
    st.plotly_chart(fig1, use_container_width=True)

with col_insight:
    st.markdown("### 💡 Insight")
    if not df_monthly.empty:
        best_month = df_monthly.loc[df_monthly['TotalPrice'].idxmax(), 'MonthName']
        best_revenue = df_monthly['TotalPrice'].max()
        worst_month = df_monthly.loc[df_monthly['TotalPrice'].idxmin(), 'MonthName']
        
        st.markdown(f"""
        **🏆 Bulan Terbaik:**  
        {best_month}  
        £{best_revenue:,.0f}
        
        **📉 Bulan Terendah:**  
        {worst_month}
        
        **📊 Total Bulan:**  
        {len(df_monthly)} bulan
        """)

st.markdown("---")

# Row dengan 2 grafik
col1, col2 = st.columns(2)

# Grafik 2: Top 10 Products by Revenue
with col1:
    st.subheader("🏆 Top 10 Produk Terlaris")
    
    df_products = df_filtered.groupby('Description').agg({
        'TotalPrice': 'sum',
        'Quantity': 'sum',
        'InvoiceNo': 'nunique'
    }).reset_index().nlargest(10, 'TotalPrice')
    
    fig2 = px.bar(
        df_products,
        y='Description',
        x='TotalPrice',
        orientation='h',
        color='TotalPrice',
        color_continuous_scale='Viridis',
        labels={'TotalPrice': 'Revenue (£)', 'Description': 'Product'},
        hover_data={'TotalPrice': ':,.0f', 'Quantity': ':,', 'InvoiceNo': ':,'}
    )
    
    fig2.update_layout(
        height=450,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'},
        coloraxis_showscale=False,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    fig2.update_traces(
        hovertemplate='<b>%{y}</b><br>Revenue: £%{x:,.0f}<br>Qty: %{customdata[0]:,}<br>Orders: %{customdata[1]:,}<extra></extra>'
    )
    
    st.plotly_chart(fig2, use_container_width=True)

# Grafik 3: Revenue by Category
with col2:
    st.subheader("📊 Revenue per Kategori")
    
    df_category = df_filtered.groupby('Category').agg({
        'TotalPrice': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    fig3 = px.pie(
        df_category,
        values='TotalPrice',
        names='Category',
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.4
    )
    
    fig3.update_traces(
        textposition='auto',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Revenue: £%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig3.update_layout(height=450, showlegend=True, legend=dict(orientation="v"))
    
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# Grafik 4: Top Countries
st.header("🌍 Revenue per Negara")

df_country = df_filtered.groupby('Country').agg({
    'TotalPrice': 'sum',
    'CustomerID': 'nunique',
    'InvoiceNo': 'nunique'
}).reset_index().sort_values('TotalPrice', ascending=True).tail(15)

fig4 = go.Figure()

fig4.add_trace(go.Bar(
    y=df_country['Country'],
    x=df_country['TotalPrice'],
    orientation='h',
    marker=dict(
        color=df_country['TotalPrice'],
        colorscale='Blues',
        showscale=True,
        colorbar=dict(title="Revenue (£)")
    ),
    text=df_country['TotalPrice'].apply(lambda x: f'£{x:,.0f}'),
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>Revenue: £%{x:,.0f}<br>Customers: %{customdata[0]:,}<br>Orders: %{customdata[1]:,}<extra></extra>',
    customdata=df_country[['CustomerID', 'InvoiceNo']].values
))

fig4.update_layout(
    height=550,
    xaxis_title="Total Revenue (£)",
    yaxis_title="Country",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig4, use_container_width=True)

# Tabel Summary yang lebih informatif
st.markdown("---")
st.header("📋 Summary Statistics per Kategori")

summary = df_filtered.groupby('Category').agg({
    'TotalPrice': ['sum', 'mean'],
    'Quantity': 'sum',
    'InvoiceNo': 'nunique',
    'CustomerID': 'nunique'
}).reset_index()

summary.columns = ['Kategori', 'Total Revenue', 'Avg Transaction', 'Total Quantity', 'Total Orders', 'Unique Customers']

# Format data
summary['Total Revenue'] = summary['Total Revenue'].apply(lambda x: f"£{x:,.2f}")
summary['Avg Transaction'] = summary['Avg Transaction'].apply(lambda x: f"£{x:,.2f}")
summary['Total Quantity'] = summary['Total Quantity'].apply(lambda x: f"{x:,}")
summary = summary.sort_values('Total Orders', ascending=False)

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Kategori": st.column_config.TextColumn("📦 Kategori", width="medium"),
        "Total Revenue": st.column_config.TextColumn("💰 Total Revenue", width="medium"),
        "Avg Transaction": st.column_config.TextColumn("💳 Avg Transaction", width="medium"),
        "Total Quantity": st.column_config.TextColumn("📊 Total Qty", width="small"),
        "Total Orders": st.column_config.NumberColumn("🧾 Orders", width="small"),
        "Unique Customers": st.column_config.NumberColumn("👥 Customers", width="small")
    }
)

# Grafik tambahan: Heatmap Hari dalam Seminggu
st.markdown("---")
st.header("📅 Pola Pembelian Berdasarkan Hari")

df_day_pattern = df_filtered.groupby('DayOfWeek').agg({
    'TotalPrice': 'sum',
    'InvoiceNo': 'nunique'
}).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()

col_day1, col_day2 = st.columns(2)

with col_day1:
    fig_day = px.bar(
        df_day_pattern,
        x='DayOfWeek',
        y='TotalPrice',
        color='TotalPrice',
        color_continuous_scale='Sunset',
        labels={'DayOfWeek': 'Hari', 'TotalPrice': 'Revenue (£)'},
        title='Revenue per Hari dalam Seminggu'
    )
    fig_day.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig_day, use_container_width=True)

with col_day2:
    fig_orders = px.bar(
        df_day_pattern,
        x='DayOfWeek',
        y='InvoiceNo',
        color='InvoiceNo',
        color_continuous_scale='Teal',
        labels={'DayOfWeek': 'Hari', 'InvoiceNo': 'Jumlah Orders'},
        title='Jumlah Orders per Hari'
    )
    fig_orders.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig_orders, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p><b>📊 Dashboard Online Retail Analytics - Enhanced Version</b></p>
    <p>Data Source: <a href='https://archive.ics.uci.edu/dataset/352/online+retail' target='_blank'>UCI Machine Learning Repository - Online Retail Dataset</a></p>
    <p>Dataset contains transactional data from UK-based online retail (2010-2011)</p>
    <p style='font-size: 0.9em; margin-top: 10px;'>💡 Gunakan filter di sidebar untuk mengeksplorasi data | Dashboard dibuat dengan Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)