from unittest import TestCase

import model.model_config as model_config
from model.data_source.data_source import CsvDataSource
from model.model_class import Model, ModelInput
from model.price_normalizer import PriceNormalizer


class ModelTestCase(TestCase):
    def test_model_on_correct_data(self):
        model = Model(
            PriceNormalizer(data_source=CsvDataSource(
                csv_path='../data/kyiv_flats_final.csv'
            )),
            model_config.input_lvs,
            model_config.output_lv,
            model_config.rule_base,
        )
        result = model.process(ModelInput(
            total_area=100.0,
            room_count=3,
            district_uk='Деснянський',
            quality=50,
            subway_time=40,
        ))
        price_fuzz = 'low'
        self.assertEqual(result.price_fuzz, price_fuzz)

    def test_model_if_a_random_district_is_selected(self):
        model = Model(
            PriceNormalizer(data_source=CsvDataSource(
                csv_path='../data/kyiv_flats_final.csv'
            )),
            model_config.input_lvs,
            model_config.output_lv,
            model_config.rule_base,
        )
        result = model.process(ModelInput(
            total_area=100.0,
            room_count=3,
            district_uk='Лісний масив',
            quality=50,
            subway_time=40,
        ))
        self.assertEqual(
            result,
            'Choose the correct district of Kyiv.',
        )

    def test_model_if_total_area_is_a_negative_number(self):
        model = Model(
            PriceNormalizer(data_source=CsvDataSource(
                csv_path='../data/kyiv_flats_final.csv'
            )),
            model_config.input_lvs,
            model_config.output_lv,
            model_config.rule_base,
        )
        result = model.process(ModelInput(
            total_area=-1,
            room_count=4,
            district_uk='Голосіївський',
            quality=1,
            subway_time=40,
        ))
        self.assertEqual(
            'Choose the right area of the apartment.',
            result,
        )

    def test_model_if_total_room_count_is_a_zero(self):
        model = Model(
            PriceNormalizer(data_source=CsvDataSource(
                csv_path='../data/kyiv_flats_final.csv'
            )),
            model_config.input_lvs,
            model_config.output_lv,
            model_config.rule_base,
        )
        result = model.process(ModelInput(
            total_area=40,
            room_count=0,
            district_uk='Голосіївський',
            quality=1,
            subway_time=40,
        ))
        self.assertEqual(
            'Choose the right number of the apartment rooms.',
            result,
        )

    def test_model_if_total_subway_time_more_than_1000_min(self):
        model = Model(
            PriceNormalizer(data_source=CsvDataSource(
                csv_path='../data/kyiv_flats_final.csv'
            )),
            model_config.input_lvs,
            model_config.output_lv,
            model_config.rule_base,
        )
        result = model.process(ModelInput(
            total_area=40,
            room_count=2,
            district_uk='Оболонський',
            quality=12,
            subway_time=10000,
        ))
        self.assertEqual(
            'Choose the right amount of time from the subway to the apartment.',
            result,
        )

    def test_how_the_model_will_behave_when_all_other_parameters_except_total_area_are_changed(self):
        model = Model(
            PriceNormalizer(data_source=CsvDataSource(
                csv_path='../data/kyiv_flats_final.csv'
            )),
            model_config.input_lvs,
            model_config.output_lv,
            model_config.rule_base,
        )

        unknown_total_area = model.process(ModelInput(
            total_area=1,
            room_count=3,
            district_uk='Деснянський',
            quality=44,
            subway_time=30,
        ))
        changed_room = model.process(ModelInput(
            total_area=1,
            room_count=1,
            district_uk='Деснянський',
            quality=44,
            subway_time=30,
        ))
        changed_quality = model.process(ModelInput(
            total_area=1,
            room_count=3,
            district_uk='Деснянський',
            quality=84,
            subway_time=30,
        ))
        changed_subway_time = model.process(ModelInput(
            total_area=1,
            room_count=3,
            district_uk='Деснянський',
            quality=44,
            subway_time=7,
        ))
        changed_district = model.process(ModelInput(
            total_area=1,
            room_count=3,
            district_uk='Подільський',
            quality=44,
            subway_time=30,
        ))

        self.assertEqual('very low', unknown_total_area.price_fuzz)
        self.assertEqual('very low', changed_room.price_fuzz)
        self.assertEqual('below medium', changed_quality.price_fuzz)
        self.assertEqual('extremely high', changed_subway_time.price_fuzz)
        self.assertEqual('low', changed_district.price_fuzz)

    def test_how_the_time_to_the_subway_affect_the_price(self):
        model = Model(
            PriceNormalizer(data_source=CsvDataSource(
                csv_path='../data/kyiv_flats_final.csv'
            )),
            model_config.input_lvs,
            model_config.output_lv,
            model_config.rule_base,
        )

        away_from_subway = model.process(ModelInput(
            total_area=100,
            room_count=2,
            district_uk='Дарницький',
            quality=80,
            subway_time=30,
        ))
        self.assertEqual('medium', away_from_subway.price_fuzz)

        near_to_subway = model.process(ModelInput(
            total_area=100,
            room_count=2,
            district_uk='Дарницький',
            quality=80,
            subway_time=5,
        ))
        self.assertEqual('low', near_to_subway.price_fuzz)

    def test_how_quality_affect_the_price(self):
        model = Model(
            PriceNormalizer(data_source=CsvDataSource(
                csv_path='../data/kyiv_flats_final.csv'
            )),
            model_config.input_lvs,
            model_config.output_lv,
            model_config.rule_base,
        )

        high_quality = model.process(ModelInput(
            total_area=40,
            room_count=3,
            district_uk='Святошинський',
            quality=85,
            subway_time=30,
        ))
        self.assertEqual('extremely high', high_quality.price_fuzz)

        low_quality = model.process(ModelInput(
            total_area=40,
            room_count=3,
            district_uk='Святошинський',
            quality=37,
            subway_time=30,
        ))
        self.assertEqual('medium', low_quality.price_fuzz)

    def test_how_district_affect_the_price(self):
        model = Model(
            PriceNormalizer(data_source=CsvDataSource(
                csv_path='../data/kyiv_flats_final.csv'
            )),
            model_config.input_lvs,
            model_config.output_lv,
            model_config.rule_base,
        )

        pechersk = model.process(ModelInput(
            total_area=40,
            room_count=3,
            district_uk='Печерський',
            quality=85,
            subway_time=30,
        ))
        self.assertEqual('above medium', pechersk.price_fuzz)

        podolsky = model.process(ModelInput(
            total_area=40,
            room_count=3,
            district_uk='Подільський',
            quality=85,
            subway_time=30,
        ))
        self.assertEqual('below medium', podolsky.price_fuzz)
