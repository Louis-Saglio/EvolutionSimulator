import time
from random import shuffle
from typing import List

import lib


def main():
    beings: List = lib.Being.build_random(1000, 4)
    constraints = {lib.Constraint.build_random() for _ in range(20)}

    assert len(beings) % 2 == 0

    start = time.time()

    for i in range(1000):

        # Get new pop
        shuffle(beings)
        beings = beings + [male.mate(female) for male, female in zip(beings, beings)]

        # Mutate
        [being.mutate() for being in beings]

        # Filter
        beings.sort(key=lambda being: sum([-constraint.apply(being) for constraint in constraints]))
        beings = beings[:len(beings) // 2]

        # Change environment
        if i % 10 == 0:
            constraints.pop()
            constraints.add(lib.Constraint.build_random())

        # Resume
        if i % 50 == 0:
            print('-' * 30, i)
            for being in beings[:5]:
                print([f"{key} : {value}" for key, value in sorted(being.genes.items())])
            for constraint in constraints:
                print(constraint)

    print(round((time.time() - start) / len(beings), 2), "second per generation")


if __name__ == '__main__':
    main()
