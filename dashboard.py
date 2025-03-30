import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    orders = pd.read_csv('orders.csv', parse_dates=['order_purchase_timestamp'])
    order_items = pd.read_csv('order_items.csv')
    order_reviews = pd.read_csv('order_reviews.csv')
    return orders, order_items, order_reviews

orders, order_items, order_reviews = load_data()

st.title("Proyek Analisis Data: Brazilian E-Commerce Public Dataset by Olist")

st.sidebar.title("Navigasi")
jenis_analisis = st.sidebar.selectbox("Pilih Analisis", ["Tren Pembelian Tahunan", "Dampak Keterlambatan Pengiriman"])

def analisis_tren_tahunan(orders, order_items):
    orders['year'] = orders['order_purchase_timestamp'].dt.year
    
    merged_data_1 = pd.merge(orders, order_items, on='order_id')
    
    pesanan_per_tahun = merged_data_1.groupby('year').size()
    return pesanan_per_tahun

def analisis_keterlambatan_pengiriman(orders, order_reviews):
    orders['is_late'] = orders['order_delivered_customer_date'] > orders['order_estimated_delivery_date']
    
    merged_data_2 = pd.merge(orders, order_reviews, on='order_id')
    
    rata_rata_ulasan = merged_data_2.groupby('is_late')['review_score'].mean()
    return rata_rata_ulasan

if jenis_analisis == "Tren Pembelian Tahunan":
    st.header("Tren Pembelian Tahunan")
    st.write("Analisis ini menunjukkan tren pembelian pelanggan dari tahun ke tahun.")
    
    pesanan_per_tahun = analisis_tren_tahunan(orders, order_items)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    pesanan_per_tahun.plot(kind='bar', color='skyblue', ax=ax)
    plt.title('Jumlah Pesanan Per Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Pesanan')
    st.pyplot(fig)

elif jenis_analisis == "Dampak Keterlambatan Pengiriman":
    st.header("Dampak Keterlambatan Pengiriman Terhadap Ulasan Pelanggan")
    st.write("Analisis ini memeriksa bagaimana keterlambatan pengiriman memengaruhi kepuasan pelanggan.")
    
    rata_rata_ulasan = analisis_keterlambatan_pengiriman(orders, order_reviews)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    rata_rata_ulasan.plot(kind='bar', color=['lightgreen', 'salmon'], ax=ax)
    plt.title('Rata-Rata Ulasan Berdasarkan Keterlambatan Pengiriman')
    plt.xlabel('Apakah Pengiriman Terlambat?')
    plt.ylabel('Rata-Rata Ulasan')
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