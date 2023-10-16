import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime


st.set_page_config(
    page_title="Dashboard Penyewaan Sepeda",
    page_icon=":bicyclist:"
)

df_day = pd.read_csv(r"day.csv")
df_hour = pd.read_csv(r"hour.csv")

df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

st.set_option('deprecation.showPyplotGlobalUse', False)

with st.sidebar:
    selected = option_menu("Homepage", ["Infografis","Hasil Analisa"], 
                           icons=['bar-chart','pie-chart-fill'], menu_icon="house", default_index=0)

    
if (selected == "Infografis"):
    st.write("# Dashboard Penyewaan Sepeda :bike:")
    
    try:
        awalDate = df_day['dteday'].min()
        akhirDate = df_day['dteday'].max()
        date_input = st.date_input(
            label='Pilih Rentang Tanggal',
            value=[awalDate, akhirDate],
            min_value=awalDate,
            max_value=akhirDate
        )
        
        if date_input[1] >= date_input[0]:
            awalDate = datetime.combine(date_input[0], datetime.min.time())
            akhirDate = datetime.combine(date_input[1], datetime.min.time())
            selisih_hari = (akhirDate - awalDate).days
        
        df_baru = df_day[:selisih_hari]
        df_hour2 = df_hour[:selisih_hari]
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Penyewa", df_baru['cnt'].sum())
        col2.metric("Member", df_baru['registered'].sum())
        col3.metric("Bukan Member", df_baru['casual'].sum())

        df_baru = df_baru.set_index('dteday', drop=False)
        plt.title('Penyewaan Sepeda Berdasarkan Hari')
        plt.plot(df_baru['casual'],c='r')
        plt.plot(df_baru['registered'],c='b')
        plt.xlabel('Hari')
        plt.xticks(rotation=45)
        plt.ylabel("Total")
        plt.legend(["Not Member", "Member"], loc="upper left")
        st.pyplot(plt.show())

        day = df_baru.groupby(by="workingday").agg({"instant": "nunique"})
        day.plot.bar(title="Perbandingan hari Libur dan hari Kerja",
                     ylabel='Total',
                     xlabel="Hari")
        st.pyplot(plt.show())


    except:
        st.error("Periksa kembali tanggal yang diinputkan")


if (selected == "Hasil Analisa"):
    pertanyaan = st.selectbox("Pilih Pertanyaan",
                              ('Tingkat Penyewaan sepeda tiap musim',
                               'Perbandingan hari kerja dan hari libur',
                               'Perbandingan Member dan Bukan',
                               'Rata - rata Suhu tiap bulan',
                               'Hubungan temperatur dan Jumlah penyewa',
                               'Tingkat penyewaan tiap jam'))
    
    if (pertanyaan == 'Tingkat Penyewaan sepeda tiap musim'):
        seasonal = df_day.groupby(by="season").agg({"cnt": "sum"})
        seasonal.plot.barh(title = "Jumlah penyewaan sepeda di setiap Musim",
                           ylabel='Musim',
                           xlabel="Total",
                           figsize=(8, 4),)
        fig = plt.show()
        st.pyplot(fig)
        st.write("# Hasil Analisa")
        st.markdown(
            """
                Berdasarkan data, dapat diketahui bahwa tingkat penyewa sepeda tertinggi ada pada musim gugur dan 
                tingkat penyewaan sepeda terendah yaitu pada musim gugur. hal ini dapat menjadi pertimbangan untuk 
                mempertambahan layanan penyewaan sepeda pada musim gugur.
            """
                    )

    if (pertanyaan == 'Perbandingan hari kerja dan hari libur'):
        daily = df_day.groupby(by="workingday").agg({"cnt": "sum"})
        daily.plot.bar(title="Penyewa Sepeda Berdasarkan Hari",
                       ylabel='Total',
                       xlabel="Hari",
                       figsize=(6, 5),)
        fig = plt.show()
        st.pyplot(fig)
        st.write("# Hasil Analisa")
        st.markdown(
            """
                Total penyewaan sepeda pada hari kerja lebih tinggi, 
                hal tersebut dikarenakan jumlah hari kerja yang lebih banyak daripada hari libur.
            """
                    )

    if (pertanyaan == 'Perbandingan Member dan Bukan'):
        member = sum(df_day['registered'])
        NotMember = sum(df_day['casual'])
        gabung = [member,NotMember]
        label = ["Member", "NotMember"]
        plt.title('Perbandingan Member dan Not Member')
        plt.pie(gabung, labels = label, autopct='%1.1f%%')
        fig = plt.show()
        st.pyplot(fig)
        st.write("# Hasil Analisa")
        st.markdown(
            """
                Sebagian besar penyewa sepeda telah melakukan registrasi.
            """
                    )
        
    if (pertanyaan == 'Rata - rata Suhu tiap bulan'):
        suhu = df_day.groupby(by="mnth").agg({"temp": ["min","max","mean"]})
        bulan = df_day['mnth'].unique()
        tempmean= suhu['temp']['mean']
        tempmin = suhu['temp']['min']
        tempmax = suhu['temp']['max']
        plt.bar(x = bulan, height=tempmax, color="red")
        plt.bar(x = bulan, height=tempmean, color="orange")
        plt.bar(x = bulan, height=tempmin, color="blue")
        plt.xlabel('Bulan')
        plt.ylabel('Temperature')
        plt.legend(['Suhu Maksimum','Suhu Rata-Rata','Suhu Minimum'],loc = 'upper left')
        fig = plt.show()
        st.pyplot(fig)
        st.write("# Hasil Analisa")
        st.markdown(
            """
                Suhu mengalami peningkatan dari bulan ke-1 hingga puncaknya pada bulan ke 7. 
                Mulai bulan ke-8 suhu terus mengalami penurunan tiap bulannya hingga bulan ke-12. 
                Pada bulan ke-5 sampai dengan bulan ke-9 merupakan bulan dengan rata rata suhu tertinggi..
            """
                    )

    if (pertanyaan == 'Hubungan temperatur dan Jumlah penyewa'):
        df_baru = df_day.drop(['instant','casual','registered'], axis="columns")
        corr = df_baru.corr(method='pearson').round(2)
        st.write(corr)

        plt.scatter(df_day['temp'], df_day['cnt'], c='blue')
        plt.title('Sebaran Data Penyewa berdasarkan Temp')
        plt.xlabel('temp')
        plt.ylabel('cnt')
        fig2 = plt.show()
        st.pyplot(fig2)

        plt.scatter(df_day['atemp'],df_day['cnt'], c='purple')
        plt.title('Sebaran Data Penyewa berdasarkan Atemp')
        plt.xlabel('atemp')
        plt.ylabel('cnt')
        fig3 = plt.show()
        st.pyplot(fig3)

        st.write("# Hasil Analisa")
        st.markdown(
            """
                Suhu mengalami peningkatan dari bulan ke-1 hingga puncaknya pada bulan ke 7. 
                Mulai bulan ke-8 suhu terus mengalami penurunan tiap bulannya hingga bulan ke-12. 
                Pada bulan ke-5 sampai dengan bulan ke-9 merupakan bulan dengan rata rata suhu tertinggi.
            """
                    )
        
    if (pertanyaan == 'Tingkat penyewaan tiap jam'):
        perjam = df_hour.groupby(by="hr").agg({"cnt": 'sum'})
        notMember = df_hour.groupby(by="hr").agg({"casual": 'sum'})
        Member = df_hour.groupby(by="hr").agg({"registered": 'sum'})
        perjama = df_hour['hr'].unique()
        kategori = df_hour['hr'].unique()
        ListLabel = ['Total Penyewa', 'Bukan Member', 'Member']
        nilai = np.array([perjam['cnt'], notMember['casual'], Member['registered']])
        num_categories = len(kategori)
        bar_width = 0.2
        category_indices = np.arange(num_categories)

        plt.figure(figsize=(18, 8))
        for i, label in enumerate(ListLabel):
            plt.bar(category_indices + i * bar_width, nilai[i], bar_width, label=label)
        
        plt.xlabel('Categories')
        plt.ylabel('Values')

        for i in range(num_categories):
            for j in range(len(ListLabel)):
                plt.text(category_indices[i] + j * bar_width - 0.05, nilai[j, i] + 1, str(nilai[j, i]))

        plt.xticks(category_indices + 0.3, kategori)
        plt.legend()
        fig = plt.show()
        st.pyplot(fig)
        st.write("# Hasil Analisa")
        st.markdown(
            """
                Pada pukul 8, 17 dan 18 merupakan jam dengan tingkat penyewaan sepeda tertinggi. 
                Pada pukul 8 sampai 16 jumlah penyewa cenderung fluktuatif, sedangkan setelah pukul 18 jumlah penyewa cenderung menurun. 
                Pukul 13 sampai dengan 17 merupakan waktu favorit bukan member melakukan penyewaan sepeda.
            """
                    )
