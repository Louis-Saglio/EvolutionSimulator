from unittest import TestCase

from lib import Constraint, Being


class TestConstraint(TestCase):
    def test_build_random(self):
        Constraint.build_random()

    def test_apply(self):
        constraint = Constraint(lambda being, gene: being.genes[gene] + 1, "a")
        actual = constraint.apply(Being({"a": 1}))
        self.assertEqual(actual, 2)
