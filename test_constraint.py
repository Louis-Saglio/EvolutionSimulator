from unittest import TestCase

from lib import Order2PolynomeConstraint, Being


class TestOrder2PolynomeConstraint(TestCase):
    def test_build_random(self):
        Order2PolynomeConstraint.build_random(1)

    def test_apply(self):
        constraint = Order2PolynomeConstraint(0, 0, 1, "a")
        actual = constraint.apply(Being({"a": 1}))
        self.assertEqual(1, actual)
