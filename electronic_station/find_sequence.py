def checkio(grid):
    limit = 4

    return any((contiguous_slice_length(grid, start, direction) >= limit)
               for start in grid_points(grid)
               for direction in [left_right, top_down, down_right, down_left])


def add(point, inc):
    return list(a + b for a, b in zip(point, inc))


def point_range(start, increment, condition):
    while condition(start):
        yield start
        start = add(start, increment)


def point_count(start, increment, condition):
    return sum(1 for _ in point_range(start, increment, condition))


def in_grid(grid):
    return lambda point: point[0] < len(grid) and point[1] < len(grid[point[0]])


def grid_slice(grid, start, increment):
    return [grid[row][col] for row, col in point_range(start, increment, in_grid(grid))]


def grid_getter(grid):
    return lambda point: grid[point[0]][point[1]]


def contiguous_slice_length(grid, start, increment):
    get = grid_getter(grid)

    value = get(start)
    in_this_grid = in_grid(grid)
    same_grid_value = lambda p: in_this_grid(p) and get(p) == value
    return point_count(start, increment, same_grid_value)


left_right = (0, 1)
top_down = (1, 0)
down_right = (1, 1)
down_left = (1, -1)

def grid_points(grid):
    return [(i, j) for i in range(len(grid[0])) for j in range(len(grid))]


from unittest import TestCase


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
        self.assertEqual(2, contiguous_slice_length([[1, 1]], (0, 0), (0, 1)))
        self.assertEqual(2, contiguous_slice_length([[1, 0], [1, 0]], (0, 0), (1, 0)))
        self.assertEqual(1, contiguous_slice_length([[0, 1], [2, 3]], (0, 0), (1, 1)))
        self.assertEqual(2, contiguous_slice_length([[0, 1], [2, 0]], (0, 0), (1, 1)))
        grid = [
            [2, 1, 1, 6, 1],
            [1, 3, 2, 1, 1],
            [4, 1, 1, 3, 1],
            [5, 5, 5, 5, 5],
            [1, 1, 3, 1, 1]
        ]
        self.assertEqual(5, contiguous_slice_length(grid, (3, 0), (0, 1)))
        self.assertEqual(3, contiguous_slice_length(grid, (0, 4), (1, 0)))

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

        checkFalse([[6,9,1,1,6,2],[5,9,7,8,2,5],[2,1,1,7,9,8],[1,8,1,4,7,4],[7,8,5,4,5,1],[6,4,8,8,1,8]])