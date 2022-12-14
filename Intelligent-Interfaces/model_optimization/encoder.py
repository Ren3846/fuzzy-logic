from typing import List
from functools import reduce


class RuleEncoder:
    __result_term_to_bit = {
        'very low': [False, False, False],
        'low': [False, False, True],
        'below medium': [False, True, False],
        'medium': [False, True, True],
        'above medium': [True, False, False],
        'high': [True, False, True],
        'extremely high': [True, True, False],
    }

    def encode(self, results: List[str]) -> List[bool]:
        mapped_result = map(
            lambda x: self.__result_term_to_bit.get(x, [False, False, False]),
            results
        )

        return reduce(
            lambda x, y: x + y,
            mapped_result
        )

    def decode(self, results_bitstring: List[bool]) -> List[str]:
        inv_map = {str(v): k for k, v in self.__result_term_to_bit.items()}

        results = []
        for i in range(0, len(results_bitstring), 3):
            results.append(inv_map.get(str(results_bitstring[i:i + 3]),'low')) # hack, if [True, True, True] -> 'low'

        return results
