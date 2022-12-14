import pandas as pd
from abc import ABC, abstractmethod


class DataSource(ABC):
    @abstractmethod
    def provide_dataframe(self) -> pd.DataFrame:
        pass


class CsvDataSource(DataSource):
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def provide_dataframe(self) -> pd.DataFrame:
        return pd.read_csv(self.csv_path)


class PandasDataSource(DataSource):
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def provide_dataframe(self) -> pd.DataFrame:
        return self.df
