from model.data_source.data_source import DataSource
from model.normalizer import normalize_values
import numpy as np


class PriceNormalizer:
    def __init__(self, data_source: DataSource):
        self.data_source = data_source

    def normalize_price(self, price_denormalized: float):
        df = self.data_source.provide_dataframe()
        real_prices = df['real_price'].to_list()
        real_prices.append(price_denormalized)
        normalized_prices = normalize_values(np.array(real_prices), 0.0, 100.0)

        return normalized_prices[len(normalized_prices) - 1]

    def denormalize_price(self, price_normalized: float):
        df = self.data_source.provide_dataframe()
        real_prices = df['real_price'].to_numpy()
        real_prices_max = real_prices.max()
        real_prices_min = real_prices.min()

        normalized_prices = normalize_values(real_prices, 0.0, 100.0)
        normalized_prices = np.append(normalized_prices, price_normalized)
        denormalized_prices = normalize_values(
            normalized_prices,
            real_prices_min,
            real_prices_max
        )

        return denormalized_prices[len(denormalized_prices) - 1]
