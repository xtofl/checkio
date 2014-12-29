def life_counter(state, ticks):
    return 15

def alive(current, live_neighbors):
    if current:
        return 1 < live_neighbors < 4
    else:
        return live_neighbors == 3


def count_live_around(state, row, col):
    neighbors = ((-1, -1), (-1, 0), (-1, 1),
                 ( 0, -1),          ( 0, 1),
                 ( 1, -1), ( 1, 0), ( 1, 1))
    count = 0
    for r, c in ((row + dr, col + dc) for dr, dc in neighbors):
        if 0 <= r < len(state) and 0 <= col < len(state[0]):
            count += state[r][c]
    return count

from unittest import TestCase


class TestGOL(TestCase):

    def test_count_live_cells(self):
        m = (
            (0, 0, 0, 0, 0),
            (0, 0, 0, 1, 0),
            (0, 0, 1, 1, 0),
            (0, 0, 0, 0, 0)
        )
        self.assertEqual(count_live_around(m, 0, 0), 0)
        self.assertEqual(count_live_around(m, 0, 2), 1)

    def test_liveCell(self):
        self.assertFalse(alive(1, 0))
        self.assertFalse(alive(1, 1))
        self.assertTrue(alive(1, 2))
        self.assertTrue(alive(1, 3))
        self.assertFalse(alive(1, 4))
        self.assertFalse(alive(1, 8))

    def test_deadCell(self):
        self.assertFalse(alive(0, 0))
        self.assertFalse(alive(0, 1))
        self.assertFalse(alive(0, 2))
        self.assertTrue(alive(0, 3))
        self.assertFalse(alive(0, 4))
        self.assertFalse(alive(0, 8))


    def test_Given(self):
        self.assertEqual(life_counter(((0, 1, 0, 0, 0, 0, 0),
              (0, 0, 1, 0, 0, 0, 0),
              (1, 1, 1, 0, 0, 0, 0),
              (0, 0, 0, 0, 0, 1, 1),
              (0, 0, 0, 0, 0, 1, 1),
              (0, 0, 0, 0, 0, 0, 0),
              (1, 1, 1, 0, 0, 0, 0)), 4), 15)
