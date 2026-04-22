import pandas as pd
import matplotlib.pyplot as plt
import seaborn as st_sns
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("all_data.zip") # Pastikan datanya sudah yang terbaru
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

all_data_df = load_data()

# --- FITUR INTERAKTIF: FILTER RENTANG WAKTU DI SIDEBAR ---
min_date = all_data_df['order_purchase_timestamp'].min()
max_date = all_data_df['order_purchase_timestamp'].max()

with st.sidebar:
    st.title("🛍️ E-Commerce Dashboard")
    st.write("**Oleh:** Karin Galuh Dea Pramesti")
    st.markdown("---")
    
    # Menambahkan Date Input
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# --- FILTERING DATA BERDASARKAN INPUT USER ---
main_df = all_data_df[(all_data_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
                      (all_data_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))]

# --- MAIN CONTENT ---
st.header("Dashboard Analisis Penjualan E-Commerce")

tab1, tab2 = st.tabs(["Performa Kategori Produk", "Tren Penjualan Bulanan (2017)"])

with tab1:
    st.subheader("Kategori Produk Terlaris dan Kurang Diminati")
    
    category_sales = main_df.groupby("product_category_name_english").order_id.nunique().sort_values(ascending=False).reset_index()
    category_sales.rename(columns={"order_id": "total_orders"}, inplace=True)

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(x="total_orders", y="product_category_name_english", data=category_sales.head(5), palette=colors, ax=ax[0])
    ax[0].set_xlabel("Jumlah Pesanan")
    ax[0].set_title("5 Kategori Teratas", loc="center", fontsize=15)

    sns.barplot(x="total_orders", y="product_category_name_english", data=category_sales.sort_values(by="total_orders", ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].set_xlabel("Jumlah Pesanan")
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("5 Kategori Terbawah", loc="center", fontsize=15)

    st.pyplot(fig)

with tab2:
    st.subheader("Tren Jumlah Pesanan per Bulan Sepanjang 2017")
    
    orders_2017 = main_df[main_df['order_purchase_timestamp'].dt.year == 2017]
    monthly_orders = orders_2017.resample(rule='ME', on='order_purchase_timestamp').agg({"order_id": "nunique"}).reset_index()
    monthly_orders['month_name'] = monthly_orders['order_purchase_timestamp'].dt.strftime('%B')

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(monthly_orders["month_name"], monthly_orders["order_id"], marker='o', linewidth=2, color="#72BCD4")
    ax2.set_title("Jumlah Pesanan Bulanan (2017)", loc="center", fontsize=20)
    plt.xticks(rotation=45)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    
    st.pyplot(fig2)