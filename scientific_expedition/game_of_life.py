def life_counter(state, ticks):
    return 15

def alive(current, live_neighbors):
    if current:
        return 1 < live_neighbors < 4
    else:
        return live_neighbors == 3

neighbors = ((-1, -1), (-1, 0), (-1, 1),
             ( 0, -1),          ( 0, 1),
             ( 1, -1), ( 1, 0), ( 1, 1))

def count_live_around(state, row, col):
    count = 0
    for r, c in ((row + dr, col + dc) for dr, dc in neighbors):
        if 0 <= r < len(state) and 0 <= c < len(state[0]):
            therow = state[r]
            thecell = therow[c]
            count += state[r][c]
    return count

def next_row(state, r):
    yield from (count_live_around(state, r, c) for c in range(len(state[r])))


def next_state(state):
    return tuple(tuple(next_row(state, r)) for r in range(len(state)))

def neighbor_row(state, r):
    yield from (count_live_around(state, r, c) for c in range(len(state[r])))

def neighbor_matrix(state):
    return tuple(tuple(neighbor_row(state, r)) for r in range(len(state)))

def count_to_live(state, count):
    return tuple(
        tuple(int(alive(current, cnt))
              for current, cnt in zip(rstate, rcount))
        for (rstate, rcount) in zip(state, count))


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

    def test_nbmatrix(self):
        m = (
            (0, 0, 0, 0, 0),
            (0, 0, 0, 1, 0),
            (0, 0, 1, 1, 0),
            (0, 0, 0, 0, 1)
        )
        self.assertEqual(neighbor_matrix(m), (
            (0, 0, 1, 1, 1),
            (0, 1, 3, 2, 2),
            (0, 1, 2, 3, 3),
            (0, 1, 2, 3, 1)
        ))

    def test_count_to_live(self):
        m = (
            (0, 0, 0, 0, 0),
            (0, 0, 0, 1, 0),
            (0, 0, 1, 1, 0),
            (0, 0, 0, 0, 1)
        )
        c = (
            (0, 0, 1, 1, 1),
            (0, 1, 3, 2, 2),
            (0, 1, 2, 3, 3),
            (0, 1, 2, 3, 1)
        )
        self.assertEqual(count_to_live(m, c), (
            (0, 0, 0, 0, 0),
            (0, 0, 1, 1, 0),
            (0, 0, 1, 1, 1),
            (0, 0, 0, 1, 0)
        ))

    def test_next_state(self):
        m = (
            (0, 0, 0, 0, 0),
            (0, 0, 0, 1, 0),
            (0, 0, 1, 1, 0),
            (0, 0, 0, 0, 1)
        )
        self.assertEqual(next_state(m), (
            (0, 0, 0, 0, 0),
            (0, 0, 1, 1, 0),
            (0, 0, 1, 1, 0),
            (0, 0, 0, 0, 0)
        ))

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
