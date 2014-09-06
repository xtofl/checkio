
def valid(grid, coord):
    if not coord: return True
    return len(grid) > coord[0] and valid(grid[coord[0]], coord[1:])

def resolve(grid, coord):
    if len(coord) == 1:
        return grid[coord[0]]
    else:
        return resolve(grid[coord[0]], coord[1:])

def slice(grid, start, step):
    current = start
    while valid(grid, current):
        yield resolve(grid, current)
        current = [a + b for a, b in zip(current, step)]


from unittest import TestCase

class STestCase(TestCase):
    def assertSEqual(self, s1, s2):
        return super().assertEqual(list(s1), list(s2))

class TestSlice2D(STestCase):

    def test_Valid(self):
        self.assertTrue(valid([], []))
        self.assertTrue(valid([1], (0)))
        self.assertFalse(valid([1], (1,)))
        self.assertTrue(valid([[], [1, 2]], (1, 1)))
        self.assertFalse(valid([[], [1, 2]], (0, 1)))

    def test_One(self):
        self.assertSEqual([1, 2], slice([1, 2], (0,), (1,)))

        grid = [[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]]
        self.assertSEqual([1, 2, 3], slice(grid, (0, 0), (0, 1)))
        self.assertSEqual([2, 3], slice(grid, (0, 1), (0, 1)))
        self.assertSEqual([1, 5, 9], slice(grid, (0, 0), (1, 1)))
        self.assertSEqual([3, 5, 7], slice(grid, (0, 2), (1, -1)))

down = (1, 0)
right = (0, 1)
down_right = (1, 1)
down_left = (1, -1)
column = lambda grid, col: slice(grid, (0, col), down)
vertical = lambda grid, side, col: [side]*3 == list(column(grid, col))
horizontal = lambda grid, side, row: [side]*3 == list(slice(grid, (row, 0), right))
diagonal1 = lambda grid, side: [side]*3 == list(slice(grid, (0, 0), down_right))
diagonal2 = lambda grid, side: [side]*3 == list(slice(grid, (0, 2), down_left))
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

class Test(STestCase):

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
