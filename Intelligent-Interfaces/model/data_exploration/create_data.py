import pandas as pd
import numpy as np

df = pd.read_csv("../../data/kyiv_flats_final_1.csv")
df_croped = df[(df.real_price < df.real_price.quantile(.95)) & (
        df.real_price > df.real_price.quantile(.05))]

total_area_noise = np.random.normal(
    df['total_area'].mean(),
    df['total_area'].std(),
    len(df.index)
)
quality_noise = np.random.normal(
    df['quality'].mean(),
    df['quality'].std(),
    len(df.index)
)
subway_time_noise = np.random.normal(
    df['subway_time'].mean(),
    df['subway_time'].std(),
    len(df.index)
)
real_price_noise = np.random.normal(
    df_croped['real_price'].mean(),
    df_croped['real_price'].std(),
    len(df.index)
)
room_count_noise = (np.random.normal(
    df['room_count'].mean(),
    df['room_count'].std(),
    len(df.index)
))

total_area_min = np.full(len(df.index), df['total_area'].min())
total_area_max = np.full(len(df.index), df['total_area'].max())

quality_min = np.full(len(df.index), df['quality'].min())
quality_max = np.full(len(df.index), df['quality'].max())

subway_time_min = np.full(len(df.index), df['subway_time'].min())
subway_time_max = np.full(len(df.index), df['subway_time'].max())

real_price_min = np.full(len(df.index), df_croped['real_price'].min())
real_price_max = np.full(len(df.index), df_croped['real_price'].max())

room_count_min = np.full(len(df.index), df['room_count'].min())
room_count_max = np.full(len(df.index), df['room_count'].max())

df['total_area'] = np.fmax(
    np.fmin(total_area_noise.round(), total_area_max),
    total_area_min
)
df['quality'] = np.fmax(
    np.fmin(quality_noise.round(), quality_max),
    quality_min
)
df['subway_time'] = np.fmax(
    np.fmin(subway_time_noise.round(), subway_time_max),
    np.round(subway_time_min) + np.random.randint(1, 3, len(df.index), int)
)
df['room_count'] = np.fmax(
    np.fmin(room_count_noise.round(), room_count_max),
    room_count_min
)
df['real_price'] = np.fmax(
    np.fmin(real_price_noise.round(), real_price_max),
    real_price_min
)
df.to_csv("../../data/kyiv_flats_final.csv", index=False)
