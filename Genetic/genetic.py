
from __future__ import annotations
import random

N_POPULATION = 200
N_SELECTED = 50
MUTATION_PROBABILITY = 0.4
random.seed(random.randint(0, 1000))


class Genetic():

    def __init__(self, genes : str, target : str, debug : bool = False):
        if N_POPULATION < N_SELECTED:
            raise ValueError(f'{N_POPULATION} must be bigger than {N_SELECTED}')
        self.debug = debug
        self.target = target
        self.population = [random.choice(genes) for _ in range(len(target))]
        self.generation, self.total_population = 0, 0
        
        
    def evaluate(item: str, main_target: str):
        """
        Counting each char in the right position
        >>> evaluate("Helxo Worlx", Hello World)
        ["Helxo Worlx", 9]
        """
        score = len(
            [g for position, g in enumerate(item) if g == main_target[position]]
        )
        return (item, float(score))
        
    def run(self):
        self.generation += 1
        self.total_population += len(self.population)
        self.population_score = [self.evaluate(item, self.target) for item in self.population]

        # Check if there is a matching evolution
        self.population_score = sorted(self.population_score, key=lambda x: x[1], reverse=True)
        if self.population_score[0][0] == self.target:
            return (self.generation, self.total_population, self.population_score[0][0])

        if self.debug and self.generation % 10 == 0:
            print(
                f"\nGeneration: {self.generation}"
                f"\nTotal Population:{self.total_population}"
                f"\nBest score: {self.population_score[0][1]}"
                f"\nBest string: {self.population_score[0][0]}"
            )

        population_best = self.population[: int(N_POPULATION / 3)]
        self.population.clear()
        self.population.extend(population_best)
        
        # Normalize population score from 0 to 1
        self.population_score = [(item, score / len(self.target)) for item, score in self.population_score]
        
        # Selection
        for i in range(N_SELECTED):
            self.population.extend(self.select(self.population_score[int(i)]))
            if len(self.population) > N_POPULATION:
                break
            

    # Select, Crossover and Mutate a new population
    def select(self, parent_1: tuple[str, float]):
        """Select the second parent and generate new population"""
        population = []
        # Generate more child proportionally to the fitness score
        child_n = int(parent_1[1] * 100) + 1
        child_n = 10 if child_n >= 10 else child_n
        for _ in range(child_n):
            parent_2 = self.population_score[random.randint(0, N_SELECTED)][0]
            child_1, child_2 = self.crossover(parent_1[0], parent_2)
            population.append(self.mutate(child_1))
            population.append(self.mutate(child_2))
        return population

    def crossover(self, parent_1: str, parent_2: str):
        """Slice and combine two string in a random point"""
        random_slice = random.randint(0, len(parent_1) - 1)
        child_1 = parent_1[:random_slice] + parent_2[random_slice:]
        child_2 = parent_2[:random_slice] + parent_1[random_slice:]
        return (child_1, child_2)

    def mutate(self, child: str):
        """Mutate a random gene of a child with another one from the list"""
        child_list = list(child)
        if random.uniform(0, 1) < MUTATION_PROBABILITY:
            child_list[random.randint(0, len(child)) - 1] = random.choice(self.genes)
        return "".join(child_list)

