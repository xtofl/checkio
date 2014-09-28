
def item(grid, coord):
    if len(coord) == 1:
        return grid[coord[0]]
    else:
        return item(grid[coord[0]], coord[1:])


def valid(grid, coord):
    return (not coord) or \
        ((len(grid) > coord[0]) and valid(grid[coord[0]], coord[1:]))


def sliced(grid, start, step):
    current = start
    while valid(grid, current):
        yield item(grid, current)
        current = [a + b for a, b in zip(current, step)]

def make_sliced(start, step):
    return lambda grid: list(sliced(grid, start, step))

down = (1, 0)
right = (0, 1)
down_right = (1, 1)
down_left = (1, -1)

def checkio(grid):
    wins = lambda side: \
        any([[side]*3 in [slice_of(grid) for slice_of in
             [make_sliced((0, i), down) for i in [0, 1, 2]] +
             [make_sliced((i, 0), right) for i in [0, 1, 2]] +
             [make_sliced((0, 0), down_right)] +
             [make_sliced((0, 2), down_left)]]])

    for side in "XO":
        if wins(side):
            return side

    return "D"

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
        self.assertSEqual([1, 2], sliced([1, 2], (0,), (1,)))

        grid = [[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]]
        self.assertSEqual([1, 2, 3], sliced(grid, (0, 0), (0, 1)))
        self.assertSEqual([2, 3], sliced(grid, (0, 1), (0, 1)))
        self.assertSEqual([1, 5, 9], sliced(grid, (0, 0), (1, 1)))
        self.assertSEqual([3, 5, 7], sliced(grid, (0, 2), (1, -1)))

class Test(STestCase):

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
