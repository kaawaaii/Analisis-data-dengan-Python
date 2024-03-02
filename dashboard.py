import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Menyiapkan data day_df
df_day = pd.read_csv("https://raw.githubusercontent.com/kaawaaii/Analisis-data-dengan-Python/main/day.csv")

# Mengubah Nama kolom
df_day.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'hr': 'hour',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Mengubah angka menjadi keterangan
df_day['month'] = df_day['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
df_day['season'] = df_day['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
df_day['weekday'] = df_day['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
df_day['weather_cond'] = df_day['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Heavy Rain/Thunderstrom'
})

# create_hour_rent_df() bertanggung jawab untuk menyiapkan hour_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# create_daily_casual_rent_df() bertanggung jawab untuk menyiapkan hour_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# create_daily_registered_rent_df() bertanggung jawab untuk menyiapkan hour_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

# create_weekday_rent_df untuk Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# create_workingday_rent_df untuk Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# create_holiday_rent_df untuk Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# create_season_rent_df untuk Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by=["month", "year"]).agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Mempersiapkan komponen filter
min_date = pd.to_datetime(df_day['dateday']).dt.date.min()
max_date = pd.to_datetime(df_day['dateday']).dt.date.max()

with st.sidebar:
    st.image('https://image.shutterstock.com/image-vector/bike-stand-rental-bicycles-electric-260nw-1789042652.jpg')

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df_day[(df_day['dateday'] >= str(start_date)) &
                 (df_day['dateday'] <= str(end_date))]

# Menyiapkan dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)

# Membuat Dashboard

# judul
st.header('Bike Rental Center')

# Membuat jumlah penyewaan Perjam
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Pengguna Casual', value=daily_rent_casual)
    st.dataframe(daily_casual_rent_df)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Pengguna registered', value=daily_rent_registered)
    st.dataframe(daily_registered_rent_df)

with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Jumlah Total Pengguna', value=daily_rent_total)
    st.dataframe(daily_rent_df)

# Jumlah penyewaan berdasarkan weekday, working dan holiday
st.subheader('Weekday, Workingday, and Holiday Rentals')
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 10))

colors1 = ["tab:green", "tab:blue", "tab:brown", "tab:pink", "tab:gray", "tab:brown", "tab:red"]
colors2 = ["tab:green", "tab:blue"]
colors3 = ["tab:green", "tab:blue"]

# Weekday
sns.barplot(
    x='weekday',
    y='count',
    data=weekday_rent_df,
    palette=colors1,
    ax=axes[0])

for index, row in enumerate(weekday_rent_df['count']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Jumlah Penyewa Berdasarkan Weekday')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

# Workingday
sns.barplot(
    x='workingday',
    y='count',
    data=workingday_rent_df,
    palette=colors2,
    ax=axes[1])

for index, row in enumerate(workingday_rent_df['count']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Jumlah Penyewa berdasarkan Hari Kerja')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

# Holiday
sns.barplot(
    x='holiday',
    y='count',
    data=holiday_rent_df,
    palette=colors3,
    ax=axes[2])

for index, row in enumerate(holiday_rent_df['count']):
    axes[2].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[2].set_title('Number of Rents based on Holiday')
axes[2].set_ylabel(None)
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)
st.dataframe(weekday_rent_df)
st.dataframe(workingday_rent_df)
st.dataframe(holiday_rent_df)

# st.subheader('Jumlah total sepeda yang disewakan berdasarkan Musim dan tahun')
# fig, ax = plt.subplots(figsize=(16, 8))
#
# df_day['month'] = pd.Categorical(df_day['weather_cond'], categories=
# ['Clear/Partly Cloudy','Misty/Cloudy','Light Snow/Rain','Heavy Rain/Thunderstrom'],
# ordered=True)
#
# season_counts = df_day.groupby(by=["season","year"]).agg({
# "count": "sum"
# }).reset_index()
#
# sns.lineplot(
# data=season_counts,
# x="season",
# y="count",
# hue="year",
# palette="rocket",
# marker="o")
#
# axes[0].set_title('Jumlah total sepeda yang disewakan berdasarkan Musim dan tahun')
# axes[0].set_ylabel(None)
# axes[0].tick_params(axis='x', labelsize=15)
# axes[0].tick_params(axis='y', labelsize=10)
#
# plt.tight_layout()
# st.pyplot(fig)

st.subheader('Jumlah total sepeda yang disewakan berdasarkan Bulan dan tahun')
fig, ax = plt.subplots(figsize=(16, 8))

monthly_counts = df_day.groupby(by=["month", "year"]).agg({
    "count": "sum"
}).reset_index()

sns.lineplot(
    data=monthly_counts,
    x="month",
    y="count",
    hue="year",
    palette="rocket",
    marker="o")

axes[0].set_title('Jumlah total sepeda yang disewakan berdasarkan Bulan dan tahun')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

plt.legend(title="Tahun", loc="upper right")
plt.tight_layout()
st.pyplot(fig)

st.subheader('Hubungan Kecepatan Angin dengan Jumlah Pengguna Terdaftar')
fig, ax = plt.subplots(figsize=(16, 8))

sns.scatterplot(
    data=df_day,
    x="windspeed",
    y="registered",
    palette="rocket",
    marker="o")

axes[0].set_title('Hubungan Kecepatan Angin dengan Jumlah Pengguna Terdaftar')
axes[0].set_ylabel('Total Pengguna Terdaftar')
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

st.subheader('Jumlah Sewa Sepeda Teregistrasi pada Hari Kerja')
fig, ax = plt.subplots(figsize=(16, 8))

filtered_data = df_day[(df_day["workingday"] == 1) & (df_day["registered"] > 0)]

sns.barplot(
    data=filtered_data,
    x="weekday",
    y="registered")

axes[0].set_title('Hubungan Kecepatan Angin dengan Jumlah Pengguna Terdaftar')
axes[0].set_ylabel('Total Pengguna Terdaftar')
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

st.subheader('Jumlah Pengguna Sepeda berdasarkan waktu Hari')

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x='weekday',
    y='count',
    data=df_day)

axes[0].set_title('Jumlah Pengguna Sepeda berdasarkan waktu Hari')
axes[0].set_xlabel('Waktu/Jam')
axes[0].set_ylabel('Jumlah Pengguna Sepeda')
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

st.subheader('Jumlah total sepeda yang disewakan berdasarkan Musim dan tahun')
fig, ax = plt.subplots(figsize=(16, 8))

df_day['month'] = pd.Categorical(df_day['weather_cond'], categories=
    ['Clear/Partly Cloudy', 'Misty/Cloudy', 'Light Snow/Rain', 'Heavy Rain/Thunderstrom'],
    ordered=True)

season_counts = df_day.groupby(by=["season", "year"]).agg({
    "count": "sum"
}).reset_index()

sns.lineplot(
    data=season_counts,
    x="season",
    y="count",
    hue="year",
    palette="rocket",
    marker="o")

axes[0].set_title('Jumlah total sepeda yang disewakan berdasarkan Musim dan tahun')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

# Displaying the dataframes
st.dataframe(season_rent_df)
st.dataframe(monthly_rent_df)
