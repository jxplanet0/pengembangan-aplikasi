###🛒 Dashboard Analisis Online Retail
Dashboard interaktif untuk menganalisis data transaksi retail online menggunakan Streamlit dan Plotly.
###📋 Deskripsi
Dashboard ini menyediakan visualisasi dan analisis komprehensif dari dataset Online Retail UCI, yang berisi transaksi retail online dari UK periode 2010-2011. Dashboard dilengkapi dengan berbagai KPI, grafik interaktif, dan filter untuk eksplorasi data yang mendalam.
###✨ Fitur Utama
##📊 Key Performance Indicators (KPI)

Total Revenue: Pendapatan total dengan perbandingan Year-over-Year (YoY)
Total Orders: Jumlah transaksi unik dan total items terjual
Unique Customers: Jumlah pelanggan unik dengan Average Revenue Per Customer (ARPC)
Average Order Value (AOV): Nilai rata-rata per transaksi

##📈 Visualisasi Data

Tren Revenue Bulanan: Grafik line chart dengan insight bulan terbaik/terendah
Top 10 Produk Terlaris: Bar chart horizontal produk dengan revenue tertinggi
Revenue per Kategori: Pie chart distribusi pendapatan berdasarkan kategori produk
Revenue per Negara: Bar chart pendapatan dari berbagai negara
Pola Pembelian Harian: Analisis pola pembelian berdasarkan hari dalam seminggu
Summary Statistics: Tabel ringkasan statistik per kategori

##🔍 Filter Interaktif

Filter berdasarkan tahun
Filter berdasarkan negara (Top 10)
Filter berdasarkan kategori produk

##🛠️ Teknologi yang Digunakan

Python 3.10+
Streamlit: Framework untuk membuat web app interaktif
Pandas: Manipulasi dan analisis data
Plotly: Visualisasi data interaktif
NumPy: Komputasi numerik



###📦 Instalasi
#1. Clone atau Download Repository
```bash
git clone <repository-url>
cd online-retail-dashboard
```
#2. Install Dependencies
```bash
bashpip install -r requirements.txt
```
Atau install manual:
```bash
pip install streamlit pandas plotly numpy
```
#3. Download Dataset
Download dataset dari UCI Machine Learning Repository dan simpan sebagai online-retail-dataset.csv di direktori yang sama dengan aplikasi.
Struktur file yang diperlukan:
```text
online-retail-dashboard/
│
├── 8.py                          # File aplikasi Streamlit
├── online-retail-dataset.csv       # Dataset (download terpisah)
├── requirements.txt                # Dependencies
└── README.md                       # File ini
```
🚀 Cara Menjalankan

```bash
streamlit run app.py
```
Dashboard akan terbuka otomatis di browser pada alamat http://localhost:8501
