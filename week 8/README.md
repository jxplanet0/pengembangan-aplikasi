# 🛒 Dashboard Analisis Online Retail
Dashboard interaktif untuk menganalisis data transaksi retail online menggunakan Streamlit dan Plotly.

# 📋 Deskripsi
Dashboard ini menyediakan visualisasi dan analisis komprehensif dari dataset Online Retail UCI, yang berisi transaksi retail online dari UK periode 2010-2011. Dashboard dilengkapi dengan berbagai KPI, grafik interaktif, dan filter untuk eksplorasi data yang mendalam.

# ✨ Fitur Utama

## 📊 Key Performance Indicators (KPI)

Total Revenue: Pendapatan total dengan perbandingan Year-over-Year (YoY)
Total Orders: Jumlah transaksi unik dan total items terjual
Unique Customers: Jumlah pelanggan unik dengan Average Revenue Per Customer (ARPC)
Average Order Value (AOV): Nilai rata-rata per transaksi

## 📈 Visualisasi Data

Tren Revenue Bulanan: Grafik line chart dengan insight bulan terbaik/terendah
Top 10 Produk Terlaris: Bar chart horizontal produk dengan revenue tertinggi
Revenue per Kategori: Pie chart distribusi pendapatan berdasarkan kategori produk
Revenue per Negara: Bar chart pendapatan dari berbagai negara
Pola Pembelian Harian: Analisis pola pembelian berdasarkan hari dalam seminggu
Summary Statistics: Tabel ringkasan statistik per kategori

## 🔍 Filter Interaktif

Filter berdasarkan tahun
Filter berdasarkan negara (Top 10)
Filter berdasarkan kategori produk

## 🛠️ Teknologi yang Digunakan

Python 3.10+
Streamlit: Framework untuk membuat web app interaktif
Pandas: Manipulasi dan analisis data
Plotly: Visualisasi data interaktif
NumPy: Komputasi numerik



# 📦 Instalasi

## 1. Clone atau Download Repository
```bash
git clone <repository-url>
cd online-retail-dashboard
```
## 2. Install Dependencies
```bash
bashpip install -r requirements.txt
```
Atau install manual:
```bash
pip install streamlit pandas plotly numpy
```
## 3. Download Dataset
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

# 📊 Dataset Information

Sumber: UCI Machine Learning Repository
Periode: Desember 2010 - Desember 2011
Jumlah Records: ~540,000 transaksi
Negara: 38 negara
Pelanggan Unik: ~4,300 pelanggan

# Kolom Dataset

InvoiceNo: Nomor invoice unik
StockCode: Kode produk
Description: Deskripsi produk
Quantity: Jumlah produk per transaksi
InvoiceDate: Tanggal dan waktu transaksi
UnitPrice: Harga per unit (GBP)
CustomerID: ID pelanggan unik
Country: Negara pelanggan

# 🎯 Kategori Produk
Dashboard otomatis mengkategorikan produk menjadi:

Storage & Containers: Tas, basket, box, case
Lighting: Lampu, lilin, lamp
Sets & Accessories: Set, kit, holder
Stationery & Gifts: Card, paper, wrap, gift
Decorations: Dekorasi, ornamen, bunting
Other: Produk lainnya

# 💡 Cara Menggunakan Dashboard

Filter Data: Gunakan sidebar di sebelah kiri untuk memfilter data berdasarkan tahun, negara, dan kategori produk
Lihat KPI: Perhatikan 4 KPI utama di bagian atas untuk overview cepat
Eksplorasi Grafik: Hover pada grafik untuk melihat detail data
Download Data: Klik tombol download pada grafik Plotly untuk export visualisasi
Interpretasi Insight: Baca insight otomatis yang ditampilkan di samping grafik tren revenue

# 📈 Interpretasi KPI
Total Revenue

Baik: Revenue meningkat dengan YoY positif
Perlu Perhatian: Revenue menurun atau YoY negatif

Average Order Value (AOV)

Good: AOV > £300
Low: AOV < £300

Average Revenue Per Customer (ARPC)

Semakin tinggi ARPC, semakin bernilai pelanggan tersebut
Gunakan untuk identifikasi high-value customers


# 🔧 Kustomisasi
Mengubah Threshold AOV
Edit baris ini di app.py:
```python
pythonaov_status = "Good 👍" if avg_order_value > 300 else "Low 📉"
```
Menambah Kategori Produk
Edit fungsi categorize_product() di app.py:
```python
pythondef categorize_product(desc):
    # Tambahkan kondisi kategori baru di sini
    if any(word in desc for word in ['KEYWORD1', 'KEYWORD2']):
        return 'New Category'
```
Mengubah Jumlah Top Countries
Edit baris ini di app.py:
```python
pythontop_countries = df.groupby('Country')['TotalPrice'].sum().nlargest(10).index.tolist()
```
# Ubah angka 10 sesuai kebutuhan


# 🐛 Troubleshooting
Error: File tidak ditemukan
Solusi: Pastikan file online-retail-dataset.csv berada di direktori yang sama dengan app.py
Error: Module tidak ditemukan
Solusi: Install ulang dependencies dengan pip install -r requirements.txt
Dashboard loading lambat
Solusi: Dashboard menggunakan caching (@st.cache_data), pertama kali akan lambat tapi selanjutnya akan cepat
Data tidak muncul setelah filter
Solusi: Reset filter dengan refresh halaman atau ubah kombinasi filter
