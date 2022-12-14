from typing import List
from numpy.random import rand, randint
from random import choices
from multiprocessing import Pool, cpu_count
from model_optimization.encoder import RuleEncoder
from model_optimization.objective_function import ObjectiveRules


class GaPipeline:
    def __init__(
            self,
            rule_encoder: RuleEncoder,
            objective_rules: ObjectiveRules,
            rule_length: int,
            iteration_count: int = 100,
            population_size: int = 40,
            crossover_rate: float = 0.95,
            mutation_rate: float = 0.05,
            tournament_count: int = 10
    ):
        self.rule_length = rule_length
        self.tournament_count = tournament_count
        self.objective_rules = objective_rules
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population_size = population_size
        self.iteration_count = iteration_count
        self.rule_encoder = rule_encoder

    def mutation(self, rule_encoded: List[bool]):
        for i in range(len(rule_encoded)):
            # check for a mutation
            if rand() < self.mutation_rate:
                # flip the bit
                rule_encoded[i] = not rule_encoded[i]

    def crossover(self, parent_1: List[bool], parent_2: List[bool]):
        # children are copies of parents by default
        child_1, child_2 = parent_1.copy(), parent_2.copy()
        # check for recombination
        if rand() < self.crossover_rate:
            # select crossover point that is not on the end of the string
            pt = randint(1, len(parent_1) - 2)
            # perform crossover
            child_1 = parent_1[:pt] + parent_2[pt:]
            child_2 = parent_2[:pt] + parent_1[pt:]

        return [child_1, child_2]

    def selection(
            self,
            population: List[List[bool]],
            scores: List[float]
    ):
        # first random selection
        selection_ix = randint(len(population))
        for ix in randint(0, len(population), self.tournament_count - 1):
            # check if better (e.g. perform a tournament)
            if scores[ix] < scores[selection_ix]:
                selection_ix = ix
        return population[selection_ix]

    def objective_func(self, population: List[bool]) -> float:
        return self.objective_rules.rmse(
            self.rule_encoder.decode(population)
        )

    def process(self):
        # initial population of random bitstring
        population = [
            choices([True, False], k=self.rule_length) for _ in
            range(self.population_size)
        ]

        # keep track of best solution
        best, best_eval = 0, self.objective_func(population[0])

        p = Pool(cpu_count()-2)
        # enumerate generations
        for gen in range(self.iteration_count):
            # evaluate all candidates in the population
            scores = p.map(self.objective_func, population)
            # check for new best solution
            for i in range(self.population_size):
                if scores[i] < best_eval:
                    best, best_eval = population[i], scores[i]
                    print(
                        ">%d, new best f(%s) = %.3f" % (
                            gen, population[i], scores[i])
                    )
            # select parents
            selected = [
                self.selection(population, scores) for _ in
                range(self.population_size)
            ]

            # create the next generation
            children = list()
            for i in range(0, self.population_size, 2):
                # get selected parents in pairs
                parent_1, parent_2 = selected[i], selected[i + 1]
                # crossover and mutation
                for child in self.crossover(parent_1, parent_2):
                    # mutation
                    self.mutation(child)
                    # store for next generation
                    children.append(child)
            # replace population
            population = children

        return [best, best_eval]
