

column = lambda grid, col: [row[col] for row in grid]
vertical = lambda grid, side, col: [side]*3 == list(column(grid, col))
horizontal = lambda grid, side, row: side*3 == grid[row]
diagonal1 = lambda grid, side: [side]*3 == [grid[i][i] for i in [0, 1, 2]]
diagonal2 = lambda grid, side: [side]*3 == [grid[i][2-i] for i in [0, 1, 2]]
diagonal = lambda grid, side: diagonal1(grid, side) or diagonal2(grid, side)

def checkio(grid):
    wins = lambda side: \
        any([vertical(grid, side, i) for i in [0, 1, 2]] +
            [horizontal(grid, side, i) for i in [0, 1, 2]] +
            [diagonal(grid, side)])

    if wins("X"):
        return "X"
    elif wins("O"):
        return "O"
    else:
        return "D"

from unittest import TestCase

class Test(TestCase):

    def assertSEqual(self, s1, s2):
        return self.assertEqual(list(s1), list(s2))

    def test_Column(self):
        self.assertSEqual([1, 2, 3], column([
            [1, 4, 4],
            [2, 4, 4],
            [3, 4, 4]], 0))
        self.assertSEqual([4, 6, 8], column([
            [1, 4, 4],
            [2, 4, 6],
            [3, 4, 8]], 2))

    def test_Horizontal(self):
        self.assertTrue(horizontal([
            "XXX",
            ".X.",
            "XOO"], "X", 0))

    def test_Given(self):
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

        self.assertEqual("X", checkio([
            "XXX",
            ".X.",
            "XOO"]))

        self.assertEqual("X", checkio([
            "XX.",
            ".X.",
            "XOX"]))
