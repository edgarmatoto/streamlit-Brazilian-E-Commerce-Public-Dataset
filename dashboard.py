import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_datasets():
    """
    Memuat semua dataset yang diperlukan untuk analisis.
    Ini termasuk data pesanan, item pesanan, ulasan, dan produk.
    """
    # Baca file CSV dan konversi kolom timestamp ke datetime
    orders = pd.read_csv('orders.csv', parse_dates=['order_purchase_timestamp'])
    order_items = pd.read_csv('order_items.csv')
    order_reviews = pd.read_csv('order_reviews.csv')
    products = pd.read_csv('products.csv')  # Tambahkan dataset produk
    
    return orders, order_items, order_reviews, products

orders, order_items, order_reviews, products = load_datasets()

st.title("Proyek Analisis Data: Brazilian E-Commerce Public Dataset by Olist")
st.sidebar.title("Navigasi")

# Pilihan analisis dari sidebar
jenis_analisis = st.sidebar.selectbox(
    "Pilih Jenis Analisis",
    ["Tren Pembelian Tahunan", "Dampak Keterlambatan Pengiriman"]
)

def analisis_tren_pembelian(orders_df, items_df, start_date, end_date):
    """
    Menghitung tren pembelian pelanggan berdasarkan rentang tanggal tertentu.
    """
    # Konversi input tanggal menjadi datetime agar sesuai dengan format kolom
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Filter data berdasarkan rentang tanggal
    filtered_orders = orders_df[
        (orders_df['order_purchase_timestamp'] >= start_date) & 
        (orders_df['order_purchase_timestamp'] <= end_date)
    ]
    
    filtered_orders['year'] = filtered_orders['order_purchase_timestamp'].dt.year
    
    combined_data = pd.merge(filtered_orders, items_df, on='order_id')
    
    tren_tahunan = combined_data.groupby('year').size()
    return tren_tahunan

def analisis_dampak_keterlambatan(orders_df, reviews_df, selected_category=None):
    """
    Menganalisis dampak keterlambatan pengiriman terhadap ulasan pelanggan,
    dengan opsi filter berdasarkan kategori produk.
    """
    orders_with_items = pd.merge(orders_df, order_items, on='order_id')
    orders_with_products = pd.merge(orders_with_items, products, on='product_id')
    
    # Filter berdasarkan kategori produk jika dipilih
    if selected_category and selected_category != "Semua Kategori":
        orders_with_products = orders_with_products[
            orders_with_products['product_category_name'] == selected_category
        ]
    
    # Tambahkan kolom untuk menandai apakah pengiriman terlambat
    orders_with_products['is_late'] = (
        orders_with_products['order_delivered_customer_date'] > 
        orders_with_products['order_estimated_delivery_date']
    )
    
    # Gabungkan dengan data ulasan
    combined_data = pd.merge(orders_with_products, reviews_df, on='order_id')
    
    # Hitung rata-rata ulasan berdasarkan status keterlambatan
    avg_reviews = combined_data.groupby('is_late')['review_score'].mean()
    return avg_reviews

if jenis_analisis == "Tren Pembelian Tahunan":
    st.header("Tren Pembelian Tahunan")
    st.write("""
    Bagian ini menunjukkan tren pembelian pelanggan dari tahun ke tahun.
    Anda dapat memfilter data berdasarkan rentang tanggal untuk melihat tren dalam periode tertentu.
    """)
    
    # Input rentang tanggal dari sidebar
    st.sidebar.subheader("Filter Rentang Tanggal")
    start_date = st.sidebar.date_input(
        "Tanggal Mulai", 
        value=pd.to_datetime("2016-01-01").date()
    )
    end_date = st.sidebar.date_input(
        "Tanggal Akhir", 
        value=pd.to_datetime("2018-12-31").date()
    )
    
    # Proses data dan tampilkan grafik
    tren_tahunan = analisis_tren_pembelian(orders, order_items, start_date, end_date)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    tren_tahunan.plot(kind='bar', color='skyblue', ax=ax)
    plt.title("Jumlah Pesanan Per Tahun")
    plt.xlabel("Tahun")
    plt.ylabel("Jumlah Pesanan")
    st.pyplot(fig)

elif jenis_analisis == "Dampak Keterlambatan Pengiriman":
    st.header("Dampak Keterlambatan Pengiriman Terhadap Ulasan Pelanggan")
    st.write("""
    Bagian ini menganalisis bagaimana keterlambatan pengiriman memengaruhi kepuasan pelanggan.
    Anda dapat memfilter data berdasarkan kategori produk untuk melihat dampak pada kategori tertentu.
    """)
    
    # Gabungkan dataset untuk mendapatkan daftar kategori produk
    orders_with_products = pd.merge(order_items, products, on='product_id')
    all_categories = ["Semua Kategori"] + list(orders_with_products['product_category_name'].dropna().unique())
    
    # Input kategori produk dari sidebar
    selected_category = st.sidebar.selectbox(
        "Pilih Kategori Produk", 
        all_categories
    )
    
    # Proses data dan tampilkan grafik
    avg_reviews = analisis_dampak_keterlambatan(orders, order_reviews, selected_category)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    avg_reviews.plot(kind='bar', color=['lightgreen', 'salmon'], ax=ax)
    plt.title("Rata-Rata Ulasan Berdasarkan Keterlambatan Pengiriman")
    plt.xlabel("Status Keterlambatan")
    plt.ylabel("Rata-Rata Ulasan")
    plt.xticks([0, 1], ['Tepat Waktu', 'Terlambat'], rotation=0)
    st.pyplot(fig)

st.markdown("""
### Kesimpulan
1. **Tren Pembelian Tahunan:**  
   - Jumlah pesanan cenderung meningkat dari tahun ke tahun, menunjukkan pertumbuhan bisnis yang positif.
   - Strategi pemasaran dapat difokuskan pada periode lonjakan permintaan untuk memaksimalkan pendapatan.

2. **Dampak Keterlambatan Pengiriman:**  
   - Pengiriman yang terlambat secara signifikan menurunkan kepuasan pelanggan, seperti tercermin dari ulasan yang lebih rendah.
   - Perbaikan logistik harus menjadi prioritas untuk meningkatkan loyalitas dan kepuasan pelanggan.
""")