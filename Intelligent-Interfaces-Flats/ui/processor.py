# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets


import model.model_config as model_config
from model.model_class import Model, ModelInput
from model.price_normalizer import PriceNormalizer
from model.data_source.data_source import CsvDataSource


class Processor:
    def __init__(self):
        self.model = Model(
            PriceNormalizer(data_source=CsvDataSource(
                csv_path='data/kyiv_flats_final.csv'
            )),
            model_config.input_lvs,
            model_config.output_lv,
            model_config.rule_base,
        )

    def process(self, area: float, district: str, rooms: float, time_to_subway: float, quality_status: float):
        if area > 100:
            area = 100
        if rooms > 5:
            rooms = 5
        if time_to_subway > 60:
            time_to_subway = 60
        if quality_status > 100:
            quality_status = 100
        input = ModelInput(
            total_area=area,
            room_count=rooms,
            district_uk=district,
            quality=quality_status,
            subway_time=time_to_subway
        )

        return self.model.process(input)
