def checkio(grid):
    pass

from unittest import TestCase

class Test(TestCase):
    def test_One(self):
        self.assertEqual("X", checkio([
            "X.O",
            "XX.",
            "XOO"]))
        self.assertEqual("O", checkio([
            "OO.",
            "XOX",
            "XOX"]))
        self.assertEqual("D", checkio([
            "OOX",
            "XXO",
            "OXX"]))