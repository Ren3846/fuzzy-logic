import pandas as pd

UAH_CURRENCY = 'uah'
USD_CURRENCY = 'usd'
USD_RATE = 36.5


def to_uah(row):
    if row['currency'] == USD_CURRENCY:
        return row['price'] * USD_RATE

    return row['price']


df = pd.read_csv('../../data/kyiv_flats_result.csv')
df['real_price'] = df.apply(to_uah, axis=1)
df.to_csv('kyiv_flats_result.csv', index=False)
