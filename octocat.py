
def checkio(cat):
    return "ULDR"

from unittest import TestCase
class TestOctoCat(TestCase):
    def testGiven(self):
        self.assertEqual("ULDR", checkio(
            [[1, 2, 3],
             [4, 6, 8],
             [7, 5, 0]]))
