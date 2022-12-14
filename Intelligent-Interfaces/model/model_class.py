from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any, Optional

from model.district_rate_provider import DistrictRateProvider
from model.fuzzy_logic import inference_mamdani
from model.price_normalizer import PriceNormalizer
from model.subway_time_calculator import SubwayTimeCalculator


@dataclass
class ModelInput:
    total_area: float
    district_uk: str
    room_count: int
    quality: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    subway_time: Optional[int] = None


@dataclass
class ModelOutput:
    price: float
    price_fuzz: str


class Model:
    def __init__(
            self,
            price_normalizer: PriceNormalizer,
            input_lvs: List[Dict[str, Any]],
            output_lvs: Dict[str, Any],
            rule_base: List[Tuple[Tuple, str]]
    ):
        self.input_lvs = deepcopy(input_lvs)
        self.output_lvs = deepcopy(output_lvs)

        inference_mamdani.preprocessing(
            self.input_lvs,
            self.output_lvs
        )

        self.price_normalizer = price_normalizer
        self.rule_base = rule_base

    def process(self, model_input: ModelInput):
        if model_input.district_uk not in ['Деснянський', 'Солом\'янський', 'Дарницький', 'Голосіївський',
                                           'Дніпровський', 'Оболонський', 'Подільський', 'Печерський', 'Святошинський',
                                           'Шевченківський']:
            return 'Choose the correct district of Kyiv.'
        elif model_input.total_area > 100 or model_input.total_area <= 0:
            return 'Choose the right area of the apartment.'
        elif model_input.room_count > 5 or model_input.room_count <= 0:
            return 'Choose the right number of the apartment rooms.'
        elif model_input.quality > 100 or model_input.quality <= 0:
            return 'Choose the right quality number of the apartment.'
        elif model_input.subway_time > 60 or model_input.subway_time <= 0:
            return 'Choose the right amount of time from the subway to the apartment.'

        nearest_subway_time = model_input.subway_time
        if nearest_subway_time is None:
            nearest_subway_time = SubwayTimeCalculator.calculate(
                model_input.latitude,
                model_input.longitude
            )

        nearest_subway_time = min(nearest_subway_time, 60)

        district_rate = DistrictRateProvider.get_district_rate(
            model_input.district_uk
        )

        crisp_values = (
            model_input.total_area,
            district_rate,
            model_input.room_count,
            nearest_subway_time,
            model_input.quality,
        )

        crisp_result, word = inference_mamdani.process(
            self.input_lvs,
            self.output_lvs,
            self.rule_base,
            crisp_values
        )

        price_denormalized = self.price_normalizer.denormalize_price(
            crisp_result
        )

        return ModelOutput(
            price=price_denormalized,
            price_fuzz=word
        )
