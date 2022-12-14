import pandas as pd

df = pd.read_json('../../data/realty_sale.json')

columns = ['total_area', 'district_uk', 'room_count', 'latitude', 'longitude', 'price', 'currency', 'url']
df_filtered = df[df['city_uk'] == 'Київ']
df_filtered = df_filtered[columns]
df_filtered.dropna(inplace=True)
df_filtered.reset_index()
df_filtered.to_csv('kyiv_flats_result.csv', index=False)





