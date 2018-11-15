import random
from unittest import TestCase


from lib import Being


class TestBeing(TestCase):
    
    def test_mate(self):
        random.seed(2)

        b1 = Being({"1": 1, "2": 2})
        b2 = Being({"1": 1, "3": 3})

        b3 = b1.mate(b2)
        self.assertIn("1", b3.genes)
        self.assertTrue("2" in b3.genes or "3" in b3.genes)

        b4 = b1.mate(b2)
        self.assertFalse("2" in b4.genes or "3" in b4.genes)

    def test_mutate(self):
        random.seed(3)
        b1 = Being({"1": 1}, 1.0)
        b1.mutate()
        self.assertEqual(b1.genes.get("1"), 0)
