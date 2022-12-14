import pandas as pd
import matplotlib.pyplot as plt
import model.model_config as model_config
from model.fuzzy_logic.inference_mamdani import preprocessing
from model.fuzzy_logic.fuzzifier import fuzzification
from model.normalizer import normalize_values
from typing import Dict


def plot_box_blot_districts(df: pd.DataFrame):
    print(df['district_uk'].unique())
    df.boxplot(column='real_price', by='district_uk', rot=45, fontsize=12, figsize=(10, 8))
    plt.show()


def preprocess_subway_time(subway_time: float):
    return min(subway_time, 60)


def apply_fuzzification_to_row(row, input_lvs, output_lv):
    crisp_values = (
        row['total_area'],
        model_config.district_to_rate[row['district_uk']],
        row['room_count'],
        preprocess_subway_time(row['subway_time']),
        row['quality'],
    )

    crisp_output = (
        row['real_price_norm'],
    )
    input_fuzzification = fuzzification(crisp_values, input_lvs)
    output_fuzzification = fuzzification(crisp_output, [output_lv])

    input_fuzzification[5] = output_fuzzification[0]


    return input_fuzzification


def process_fuzzy_values(fuzzy_values: Dict[int, Dict[str, float]]):
    result_terms = []
    for fuzzy_value in fuzzy_values.values():
        max_value = 0
        result_term = ''
        for term, mf_value in fuzzy_value.items():
            if mf_value > max_value:
                result_term = term
                max_value = mf_value

        result_terms.append(result_term)

    return result_terms


df: pd.DataFrame = pd.read_csv('../../data/kyiv_flats_final_1.csv')

preprocessing(model_config.input_lvs, model_config.output_lv)
df = df[(df.real_price < df.real_price.quantile(.95)) & (df.real_price > df.real_price.quantile(.05))]

df['real_price_norm'] = list(normalize_values(df['real_price'].to_numpy(), 0.0, 100.0))

result = df.apply(
    lambda x: apply_fuzzification_to_row(x, model_config.input_lvs, model_config.output_lv), axis=1)

result_filtered = map(process_fuzzy_values, result)
df[['total_area_fizz', 'district_uk_fizz', 'room_count_fizz', 'subway_time_fizz', 'quality_fizz',
    'real_price_fizz']] = list(result_filtered)
print(df[['total_area_fizz', 'district_uk_fizz', 'room_count_fizz', 'subway_time_fizz', 'quality_fizz',
    'real_price_fizz']])

