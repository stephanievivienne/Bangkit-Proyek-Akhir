import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
st.set_option('deprecation.showPyplotGlobalUse', False)

sns.set(style='dark')
data_df = pd.read_csv("https://raw.githubusercontent.com/stephanievivienne/bikedataset/main/day.csv")
data2_df = pd.read_csv("https://raw.githubusercontent.com/stephanievivienne/bikedataset/main/hour.csv")

#Data pnreprocessing
data_df.drop_duplicates(inplace=True)
data2_df.drop_duplicates(inplace=True)
data_df.fillna(method="ffill", inplace=True)
data2_df.fillna(method="ffill", inplace=True)

bike_df = data2_df.merge(data_df, on='dteday', how='inner', suffixes=('_hour', '_day'))

weather_labels = {
    1: 'Jernih',
    2: 'Kabut',
    3: 'Curah Hujan Ringan',
    4: 'Curah Hujan Lebat'
}
bike_df['weather_label'] = bike_df['weathersit_day'].map(weather_labels)

# Streamlit app
st.title('Dashboard Visualisasi Data Sepeda')

# Visualizations
st.subheader('Visualisasi Data:')

# Korelasi antara variabel numerik
corr_matrix = bike_df[['temp_hour', 'atemp_hour', 'hum_hour', 'windspeed_hour', 'cnt_hour']].corr()
st.subheader('Matriks Korelasi untuk Data Per Jam')
st.write(corr_matrix)

corr_matrix_day = bike_df[['temp_day', 'atemp_day', 'hum_day', 'windspeed_day', 'cnt_day']].corr()
st.subheader('Matriks Korelasi untuk Data Cuaca')
st.write(corr_matrix_day)

# Hubungan antara suhu dengan jumlah peminjaman
st.subheader('Suhu vs Jumlah Peminjaman (Per Jam)')
sns.scatterplot(x='temp_hour', y='cnt_hour', data=bike_df)
st.pyplot()

# Hubungan antara Kelembapan dengan jumlah peminjaman
st.subheader('Kelembapan vs Jumlah Peminjaman (Per Jam)')
sns.scatterplot(x='hum_hour', y='cnt_hour', data=bike_df)
st.pyplot()

# Hubungan antara Kecepatan angin dengan jumlah peminjaman
st.subheader('Kecepatan Angin vs Jumlah Peminjaman (Per Jam)')
sns.scatterplot(x='windspeed_hour', y='cnt_hour', data=bike_df)
st.pyplot()

# Hubungan antara kondisi cuaca dengan jumlah peminjaman
st.subheader('Kondisi Cuaca vs Jumlah Peminjaman (Per Jam)')
sns.boxplot(x='weathersit_hour', y='cnt_hour', data=bike_df)
st.pyplot()

# Visualisasi peminjaman sepeda per jam
st.subheader('Peminjaman Sepeda per Jam')
sns.lineplot(data=bike_df, x='hr', y='cnt_hour', hue='workingday_hour')
plt.xlabel('Jam')
plt.ylabel('Jumlah')
st.pyplot()

# Distribusi peminjaman sepeda
st.subheader('Distribusi Peminjaman Sepeda')
sns.histplot(data=bike_df, x='cnt_hour', bins=30, kde=True)
plt.xlabel('Jumlah')
plt.ylabel('Frekuensi')
st.pyplot()

# Line plot of rental count over time
st.write("Grafik Perubahan Jumlah Penyewaan Sepeda dari Waktu ke Waktu:")
st.line_chart(bike_df.set_index('dteday')['cnt_day'])


# Bar plot of average rental count by weather label
st.write("Rata - Rata Penyewaan Sepeda berdasarkan Kondisi Cuaca:")
st.bar_chart(bike_df.groupby('weather_label')['cnt_day'].mean())

# Bar plot of average rental count by hour
st.write("Rata - Rata Penyewaan Sepeda berdasarkan Jam:")
st.bar_chart(bike_df.groupby('hr')['cnt_hour'].mean())

# Box plot of rental count by holiday
st.write("Perbandingan Jumlah Penyewaan Sepeda pada Hari Libur dan Bukan Hari Libur:")
plt.figure(figsize=(8, 5))
sns.boxplot(x='holiday_day', y='cnt_day', data=bike_df)
plt.xlabel('Hari Libur')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.xticks([0, 1], ['Tidak Libur', 'Libur'])
st.pyplot()

# Histogram of temperature distribution
st.write("Distribusi Suhu pada Data:")
plt.hist(data_df['temp'], bins=20, edgecolor='black')
plt.xlabel('Suhu')
plt.ylabel('Frekuensi')
st.pyplot()
