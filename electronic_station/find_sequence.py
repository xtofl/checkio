from unittest import TestCase

def checkio(grid):
    return False

class Test(TestCase):
    def test_One(self):
        def checkTrue(grid):
            self.assertTrue(checkio(grid))
        def checkFalse(grid):
            self.assertFalse(checkio(grid))
        checkTrue([
            [1, 2, 1, 1],
            [1, 1, 4, 1],
            [1, 3, 1, 6],
            [1, 7, 2, 5]
        ]) == True
        checkFalse([
            [7, 1, 4, 1],
            [1, 2, 5, 2],
            [3, 4, 1, 3],
            [1, 1, 8, 1]
        ]) == False
        checkTrue([
            [2, 1, 1, 6, 1],
            [1, 3, 2, 1, 1],
            [4, 1, 1, 3, 1],
            [5, 5, 5, 5, 5],
            [1, 1, 3, 1, 1]
        ]) == True
        checkTrue([
            [7, 1, 1, 8, 1, 1],
            [1, 1, 7, 3, 1, 5],
            [2, 3, 1, 2, 5, 1],
            [1, 1, 1, 5, 1, 4],
            [4, 6, 5, 1, 3, 1],
            [1, 1, 9, 1, 2, 1]
            ]) == True