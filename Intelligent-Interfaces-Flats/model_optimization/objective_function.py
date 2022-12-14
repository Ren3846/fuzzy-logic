import pandas as pd
import numpy as np
import math
from typing import List, Tuple
import model.model_config as model_config
from model.model_class import Model, ModelInput
from model.price_normalizer import PriceNormalizer
from model.data_source.data_source import PandasDataSource


class ObjectiveRules:
    def __init__(self, df: pd.DataFrame, conditions: List[Tuple]):
        self.df = df
        self.conditions = conditions

    @staticmethod
    def apply_model_to_row(row, model: Model):
        model_result = model.process(
            ModelInput(
                total_area=row['total_area'],
                district_uk=row['district_uk'],
                room_count=row['room_count'],
                quality=row['quality'],
                subway_time=row['subway_time']
            )
        )

        return model_result.price

    def rmse(self, results: List[str]) -> float:
        rule_base = list(zip(self.conditions, results))

        model = Model(
            price_normalizer=PriceNormalizer(
                data_source=PandasDataSource(self.df)
            ),
            input_lvs=model_config.input_lvs,
            output_lvs=model_config.output_lv,
            rule_base=rule_base
        )

        real_prices = self.df['real_price'].to_numpy()
        calculated_prices = np.asarray(
            self.df.apply(
                lambda x: self.apply_model_to_row(x, model),
                axis=1
            )
        )

        mse = np.square(np.subtract(real_prices, calculated_prices)).mean()

        return math.sqrt(mse)
