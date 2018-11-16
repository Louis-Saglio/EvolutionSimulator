from __future__ import annotations

import string
from random import choice, choices, randint, random
from typing import Dict, List, Set


def get_random_string(max_size: int):
    return ''.join(choices(string.ascii_lowercase, k=max_size))


class Being:
    gene_name_max_size = 3
    gene_max_value = 1

    @classmethod
    def build_random(cls, pop_size: int, genes_max_size: int) -> List[Being]:
        beings: List[Being] = []
        for _ in range(pop_size):
            being = cls(mutation_probability=0)
            for __ in range(randint(1, genes_max_size)):
                gene_name: str = get_random_string(cls.gene_name_max_size)
                gene_value: int = randint(0, cls.gene_max_value)
                being.genes[gene_name] = gene_value
            beings.append(being)
        return beings

    def __init__(self, genes: Dict[str, int]=None, mutation_probability: float=0.02):
        self.genes = genes or {}
        self.mutation_probability = mutation_probability

    def __repr__(self):
        return f"Being[genes : {self.genes}, mutation_prob : {self.mutation_probability}]"

    def mate(self, other: Being) -> Being:
        new_being = Being()
        genes = set(self.genes)
        for gene in genes.intersection(other.genes):
            new_being.genes[gene] = choice((self.genes[gene], other.genes[gene]))
        for gene in genes.difference(other.genes):
            if choice((True, False)):
                if gene in self.genes:
                    new_gene_value = self.genes[gene]
                else:
                    new_gene_value = other.genes[gene]
                new_being.genes[gene] = new_gene_value
        return new_being

    def mutate(self):
        to_remove = set()
        to_add = {}
        for gene in self.genes:
            if random() < self.mutation_probability:
                self.mutation_probability *= choice((random(), random() + 1))
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

    def apply(self, being: Being) -> int:
        raise NotImplementedError

    def __hash__(self) -> int:
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


class Order2PolynomeConstraint(Constraint):

    @classmethod
    def build_random(cls, nbr: int) -> Set[Order2PolynomeConstraint]:
        return {
            cls(randint(-99, 99), randint(-99, 99), randint(-99, 99), get_random_string(Being.gene_name_max_size))
            for _ in range(nbr)
        }

    def __init__(self, a: int, b: int, c: int, gene: str):
        self.gene = gene
        self.a, self.b, self.c = a, b, c

    def __hash__(self):
        return hash((self.a, self.b, self.c, self.gene))

    def __repr__(self):
        # todo : show nullification point
        return "{} {}, {}, {}".format(
            self.gene,
            self.apply(Being({self.gene: -3})),
            self.apply(Being({self.gene: 0})),
            self.apply(Being({self.gene: 3}))
        )

    def apply(self, being: Being) -> int:
        value = being.genes.get(self.gene, 0)
        return self.a * value ** 2 + self.b * value + self.c
