import pandas as pd

import model.model_config as model_config
from model.model_class import Model, ModelInput
from model.price_normalizer import PriceNormalizer
from model.data_source.data_source import CsvDataSource
from model_optimization.encoder import RuleEncoder
from model_optimization.ga import GaPipeline
from model_optimization.objective_function import ObjectiveRules
from model_optimization.config import conditions

model = Model(
    PriceNormalizer(
        data_source=CsvDataSource(
            csv_path='../data/kyiv_flats_final_1.csv'
        )
    ),
    model_config.input_lvs,
    model_config.output_lv,
    model_config.rule_base,
)

if __name__ == "__main__":
    results = []
    for rule in model_config.rule_base:
        results.append(rule[1])

    rule_encoder = RuleEncoder()

    encoded = rule_encoder.encode(results)

    ga_pipeline = GaPipeline(
        rule_encoder=RuleEncoder(),
        objective_rules=ObjectiveRules(
            df=pd.read_csv("../data/kyiv_flats_final_1.csv"),
            conditions=conditions
        ),
        rule_length=len(encoded)
    )

    rules, rules_value = ga_pipeline.process()

    decoded_rules = rule_encoder.decode(rules)

    print(list(zip(conditions, decoded_rules)))
    print(f"RMSE = {rules_value}")
