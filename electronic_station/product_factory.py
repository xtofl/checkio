from unittest import TestCase

def factors(n):
    for p in [2, 3, 5, 7]:
        while n % p == 0:
            yield p
            n /= p

class TestProductFactory(TestCase):
    def test_factors(self):
        self.assertEqual([2], list(factors(2)))
        self.assertEqual([2, 2], list(factors(4)))
        self.assertEqual([2, 2, 3], list(factors(12)))