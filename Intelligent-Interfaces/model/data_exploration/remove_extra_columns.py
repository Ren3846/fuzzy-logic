import pandas as pd

result_columns = ['total_area', 'district_uk', 'room_count', 'subway_time', 'quality', 'real_price']
df = pd.read_csv('../../data/kyiv_flats_result.csv')
df[result_columns].to_csv('kyiv_flats_final_1.csv', index=False)
