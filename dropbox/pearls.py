
def checkio(marbles, N):
    prob_black = marbles.count('b') / float(len(marbles))
    prob_white = 1 - prob_black
    if N == 1:
        return prob_white
    else:
        return sum([
            prob_black * checkio(marbles.replace('b', 'w', 1), N - 1),
            prob_white * checkio(marbles.replace('w', 'b', 1), N - 1)
        ])

from unittest import TestCase

class TestPearls(TestCase):
    def test_One(self):
        self.assertAlmostEqual(0.0, checkio('bbbb', 1), places=2)
        self.assertAlmostEqual(1.0, checkio('wwww', 1), places=2)
        self.assertAlmostEqual(0.48, checkio('bbw', 3), places=2)
        self.assertAlmostEqual(0.52, checkio('wwb', 3), places=2)
        self.assertAlmostEqual(0.56, checkio('www', 3), places=2)
        self.assertAlmostEqual(0.5, checkio('wwbb', 4), places=2)
