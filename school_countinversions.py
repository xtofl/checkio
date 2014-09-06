from functools import reduce
from itertools import combinations, starmap

def count_inversion(numbers):
    is_inversion = lambda i, j: i < j and numbers[i] > numbers[j]
    inversions = [_f for _f in starmap(is_inversion, combinations(list(range(len(numbers))), 2)) if _f]
    return sum(inversions)

from unittest import TestCase
class TestCountInversions(TestCase):

    def test_Given(self):
        self.assertEqual(3, count_inversion((1, 2, 5, 3, 4, 7, 6)))
        self.assertEqual(0, count_inversion((0, 1, 2, 3)))
        self.assertEqual(1, count_inversion((99, -99)))
        self.assertEqual(10, count_inversion((5, 3, 2, 1, 0)), "Reversed")