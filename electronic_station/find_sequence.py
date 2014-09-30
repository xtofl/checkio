from unittest import TestCase

def add(point, inc):
    return list(a + b for a, b in zip(point, inc))

def horizontal(grid, start):
    pass

def point_range(start, increment, condition):
    while condition(start):
        yield start
        start = add(start, increment)

def in_grid(grid):
    def f(point):
        return point[0] < len(grid) and point[1] < len(grid[point[0]])
    return f


def grid_slice(grid, start, increment):
    return [grid[row][col] for row, col in point_range(start, increment, in_grid(grid))]


def grid_getter(grid):
    return lambda point: grid[point[0]][point[1]]


def grid_equal_row(grid, start, increment):
    get = grid_getter(grid)

    value = get(start)
    in_this_grid = in_grid(grid)
    same_grid_value = lambda p: in_this_grid(p) and get(p) == value
    return [grid[row][col] for row, col in point_range(start, increment, same_grid_value)]


left_right = (0, 1)
top_down = (1, 0)
down_right = (1, 1)
down_left = (1, -1)

def grid_points(grid):
    return [(i, j) for i in range(len(grid[0])) for j in range(len(grid))]


def checkio(grid):
    limit = 4

    return any((len(grid_equal_row(grid, start, direction)) >= limit)
               for start in grid_points(grid)
               for direction in [left_right, top_down, down_right, down_left])


class Test(TestCase):

    def test_point(self):
        self.assertEqual([1], add([1], [0]))
        self.assertEqual([1, 2, 3], add([1, 1, 1], [0, 1, 2]))

    def test_slice(self):
        width = 4
        height = 5
        grid = [range(i*width, i*width+width) for i in range(height)]
        self.assertEqual([0, 1, 2, 3], grid_slice(grid, (0, 0), (0, 1)))
        self.assertEqual([0, 4, 8, 12, 16], grid_slice(grid, (0, 0), (1, 0)))
        self.assertEqual([4, 8, 12, 16], grid_slice(grid, (1, 0), (1, 0)))
        self.assertEqual([0, 5, 10, 15], grid_slice(grid, (0, 0), (1, 1)))

    def test_equal_row(self):
        g = grid_getter([[1, 2, 3]])
        self.assertEqual(1, g((0, 0)))
        self.assertEqual(2, g((0, 1)))
        self.assertEqual(3, g((0, 2)))
        self.assertEqual([1, 1], grid_equal_row([[1, 1]], (0, 0), (0, 1)))
        self.assertEqual([1, 1], grid_equal_row([[1, 0], [1, 0]], (0, 0), (1, 0)))
        self.assertEqual([0], grid_equal_row([[0, 1], [2, 3]], (0, 0), (1, 1)))
        self.assertEqual([0, 0], grid_equal_row([[0, 1], [2, 0]], (0, 0), (1, 1)))
        grid = [
            [2, 1, 1, 6, 1],
            [1, 3, 2, 1, 1],
            [4, 1, 1, 3, 1],
            [5, 5, 5, 5, 5],
            [1, 1, 3, 1, 1]
        ]
        self.assertEqual([5, 5, 5, 5, 5], grid_equal_row(grid, (3, 0), (0, 1)))
        self.assertEqual([1, 1, 1], grid_equal_row(grid, (0, 4), (1, 0)))

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
        ])
        checkFalse([
            [7, 1, 4, 1],
            [1, 2, 5, 2],
            [3, 4, 1, 3],
            [1, 1, 8, 1]
        ])
        checkTrue([
            [2, 1, 1, 6, 1],
            [1, 3, 2, 1, 1],
            [4, 1, 1, 3, 1],
            [5, 5, 5, 5, 5],
            [1, 1, 3, 1, 1]
        ])
        checkTrue([
            [7, 1, 1, 8, 1, 1],
            [1, 1, 7, 3, 1, 5],
            [2, 3, 1, 2, 5, 1],
            [1, 1, 1, 5, 1, 4],
            [4, 6, 5, 1, 3, 1],
            [1, 1, 9, 1, 2, 1]
            ])