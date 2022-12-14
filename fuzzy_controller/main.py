import fuzzy_operators
import model
import inference_mamdani

inference_mamdani.preprocessing(model.input_lvs, model.output_lv)

# for i_1 in range(101):
#     for i_2 in range(200):
#         for i_3 in range(50):
#             for i_4 in range(0, 100_000, 1000):
#                 crisp_values = (i_1, i_2, i_3, i_4)
#                 result = inference_mamdani.process(model.input_lvs, model.output_lv, model.rule_base, crisp_values)
#                 print(crisp_values, result)

for lv in model.input_lvs:
    fuzzy_operators.draw_lv(lv)
fuzzy_operators.draw_lv(model.output_lv)



