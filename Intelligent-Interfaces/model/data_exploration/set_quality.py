import pandas as pd

df_filtered = pd.read_csv('../../data/kyiv_flats_result.csv')

quality = df_filtered['quality'].to_list()
for idx, url in enumerate(df_filtered['url']):
    if quality[idx] != 0 :
        continue
    print(idx)
    print(url)
    quality[idx] = int(input("Оцінка: "))
df_filtered['quality'] = quality
df_filtered.to_csv('kyiv_flats_result.csv', index=False)