import model.model_config as model_config
from model.model_class import Model, ModelInput
from model.price_normalizer import PriceNormalizer
from model.data_source.data_source import CsvDataSource

model = Model(
    PriceNormalizer(data_source=CsvDataSource(
        csv_path='data/kyiv_flats_final.csv'
    )),
    model_config.input_lvs,
    model_config.output_lv,
    model_config.rule_base,
)

if __name__ == "__main__":
    result = model.process(ModelInput(
        total_area=82.0,
        room_count=3,
        district_uk="Деснянський",
        quality=60,
        subway_time=163
    ))
    print(result)
