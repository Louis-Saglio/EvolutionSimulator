import time
from random import shuffle, randint
from typing import List, Set

import lib


def resume(beings, constraints, i=None):
    if i % 50 == 0:
        print('-' * 30, i if i else "")
        for constraint in constraints:
            print(constraint)
        for being in beings[:5]:
            print([f"{key} : {value}" for key, value in sorted(being.genes.items())], round(being.mutation_probability, 3))


def main():
    beings: List = lib.Being.build_random(1000, 4)
    constraints: Set[lib.Constraint] = lib.Order2PolynomeConstraint.build_random(30)

    assert len(beings) % 2 == 0

    start = time.time()

    for i in range(1000):

        # Get new pop
        shuffle(beings)
        beings = beings + [male.mate(female) for male, female in zip(beings[::-1], beings)]

        # Mutate
        [being.mutate() for being in beings]

        # Filter
        beings.sort(key=lambda being: sum([-constraint.apply(being) for constraint in constraints]))
        beings = beings[:len(beings) // 2]

        # Change environment
        if randint(1, len(constraints) * 2) == 1:
            constraints.pop()
            constraints.update(lib.Order2PolynomeConstraint.build_random(1))

        # Resume
        resume(beings, constraints, i)

    print(round((time.time() - start) / len(beings), 2), "second per generation")


if __name__ == '__main__':
    main()
