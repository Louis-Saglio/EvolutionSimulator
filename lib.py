from __future__ import annotations

from random import choice, choices, randint, random
from typing import Callable, Collection, Dict, List
import string


def get_random_string(max_size: int):
    return ''.join(choices(string.ascii_lowercase, k=max_size))


class Being:
    gene_name_max_size = 3
    gene_max_value = 1

    @classmethod
    def build_random(cls, pop_size: int, genes_max_size: int) -> Collection[Being]:
        beings: List[Being] = []
        for _ in range(pop_size):
            being = Being()
            for __ in range(randint(1, genes_max_size)):
                gene_name: str = get_random_string(cls.gene_name_max_size)
                gene_value: int = randint(0, cls.gene_max_value)
                being.genes[gene_name] = gene_value
            beings.append(being)
        return beings

    def __init__(self, genes: Dict[str, int]=None, mutation_probability: float=0.01):
        self.genes = genes or {}
        self.mutation_probability = mutation_probability

    def __repr__(self):
        return f"Being[genes : {self.genes}, mutation_prob : {self.mutation_probability}]"

    def __eq__(self, other: Being):
        return self.genes == other.genes

    def mate(self, other: Being) -> Being:
        new_being = Being()
        genes = set(self.genes)
        for gene in genes.intersection(other.genes):
            new_being.genes[gene] = choice((self.genes[gene], other.genes[gene]))
        for gene in genes.difference(other.genes):
            if choice((True, False)):
                new_being.genes[gene] = self.genes.get(gene) or other.genes.get(gene)
        return new_being

    def mutate(self):
        to_remove = set()
        to_add = {}
        for gene in self.genes:
            if random() < self.mutation_probability:
                result = choice((0, 1, 2, 3))
                if result == 0:
                    self.genes[gene] += 1
                elif result == 1:
                    self.genes[gene] -= 1
                elif result == 2:
                    to_remove.add(gene)
                elif result == 3:
                    to_add[get_random_string(Being.gene_name_max_size)] = randint(0, Being.gene_max_value)
        for gene in to_remove:
            del self.genes[gene]
        self.genes.update(to_add)


class Constraint:

    @classmethod
    def build_random(cls) -> Constraint:
        gene = get_random_string(Being.gene_name_max_size)
        a, b, c = randint(-99, 99), randint(-99, 99), randint(-99, 99)

        def func(being: Being, gene_):
            if gene_ in being.genes:
                x = being.genes[gene_]
                return a * x ** 2 + b * x + c
            return 0
        return Constraint(func, gene)

    def __init__(self, func: Callable[[Being, str], int], gene: str):
        self.gene = gene
        self.func = func

    def __hash__(self):
        return hash(self.func)

    def __repr__(self):
        # todo : show nullification point
        return "{} {}, {}, {}".format(self.gene, self.apply(Being({self.gene: -3})), self.apply(Being({self.gene: 0})), self.apply(Being({self.gene: 3})))

    def apply(self, being: Being) -> int:
        return self.func(being, self.gene)
