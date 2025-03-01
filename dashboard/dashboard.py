import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar


# Menentukan path file CSV secara dinamis
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "main_data.csv")

try:
    df = pd.read_csv(data_path)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Pastikan 'season' dan 'weekday' dalam format yang benar
if df['season'].dtype != object:
    df['season'] = df['season'].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})

if df['weekday'].dtype != object:
    df['weekday'] = df['weekday'].astype(int)
    df['weekday'] = df['weekday'].map({i: calendar.day_name[i] for i in range(7)})

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_month = st.sidebar.selectbox("Pilih Bulan", df['datetime'].dt.month_name().unique())
filtered_df = df[df['datetime'].dt.month_name() == selected_month]

# Header
st.title("Dashboard Bike Sharing")
st.write("Analisis penggunaan sepeda berdasarkan waktu dan faktor lingkungan.")

# Grafik Tren Penyewaan
st.subheader("Tren Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_df, x='datetime', y='total_count', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Pola Penggunaan Sepeda per Jam Berdasarkan Musim
st.subheader("Distribusi Penggunaan Sepeda Per Jam Berdasarkan Musim")
if 'hour' in df.columns:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.pointplot(data=df, x='hour', y='total_count', hue='season', ax=ax)
    st.pyplot(fig)
else:
    st.write("Data tidak memiliki kolom 'hour'")

# Pola Penggunaan Sepeda per Jam Berdasarkan Hari
st.subheader("Distribusi Penggunaan Sepeda Per Jam Berdasarkan Hari")
if 'hour' in df.columns:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.pointplot(data=df, x='hour', y='total_count', hue='weekday', ax=ax, hue_order=list(calendar.day_name))
    ax.legend(title="Weekday", bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)
else:
    st.write("Data tidak memiliki kolom 'hour'")
