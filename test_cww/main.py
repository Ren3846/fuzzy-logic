import model
import random
import mamdani_inference


mamdani_inference.preprocessing(model.input_lvs, model.output_lv)

for i in range(20):
    crisps = (random.randint(18, 70), random.randint(140, 200), random.randint(17, 45), random.randint(5_000, 50_000))
    res = mamdani_inference.process(model.input_lvs, model.output_lv, model.rule_base, crisps)
    print(crisps, res, sep='\t')