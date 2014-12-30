from itertools import dropwhile, takewhile


def life_counter(state, ticks):
    if ticks == 0:
        return sum(sum(r) for r in state)
    else:
        return life_counter(next_state(state), ticks - 1)

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
    enlarged = enlarge(state)
    processed = count_to_live(enlarged, neighbor_matrix(enlarged))
    return strip(processed)

def neighbor_row(state, r):
    yield from (count_live_around(state, r, c) for c in range(len(state[r])))

def neighbor_matrix(state):
    return tuple(tuple(neighbor_row(state, r)) for r in range(len(state)))

def count_to_live(state, count):
    return tuple(
        tuple(int(alive(current, cnt))
              for current, cnt in zip(rstate, rcount))
        for (rstate, rcount) in zip(state, count))


def enlarge(state):
    if not state: return tuple()
    zeroes = (0, ) * (2 + len(state[0]))
    return \
        (zeroes, ) + \
        tuple(
            (0, ) + row + (0, ) for row in state
        ) + \
        (zeroes, )

def left_margin(state):
    return min(sum(1 for _ in takewhile(lambda c: not c, row)) for row in state)

def right_margin(state):
    return min(sum(1 for _ in takewhile(lambda c: not c, reversed(row))) for row in state)

def strip(state):
    #top/bottom row
    def empty(s):
        return not s or not s[0]
    if empty(state): return tuple()

    def stripped(s):
        return tuple(dropwhile(lambda r: not any(r), s))
    stripped_top = stripped(state)
    if empty(stripped_top): return tuple()

    stripped_bottom = tuple(reversed(stripped(tuple(reversed(stripped_top)))))
    if empty(stripped_bottom): return tuple()

    left = left_margin(stripped_bottom)
    right = len(state[0]) - right_margin(stripped_bottom)
    return tuple(r[left:right] for r in stripped_bottom)

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

    def test_enlarge(self):
        self.assertEqual(enlarge(((0,),)), ((0, 0, 0), (0, 0, 0), (0, 0, 0)))
        self.assertEqual(enlarge(tuple()), tuple())

    def test_next_state(self):
        m = (
            (0, 0, 0, 0, 0),
            (0, 0, 0, 1, 0),
            (0, 0, 1, 1, 0),
            (0, 0, 0, 0, 1)
        )
        self.assertEqual(next_state(m), (
            (1, 1, 0),
            (1, 1, 1),
            (0, 1, 0)
        ))
        self.assertEqual(next_state(next_state(m)), (
            (1, 0, 1),
            (0, 0, 1),
            (1, 1, 1)
        ))
        self.assertEqual(next_state(next_state(next_state(m))), (
            (0, 1, 0, 0),
            (1, 0, 1, 1),
            (0, 1, 1, 0),
            (0, 1, 0, 0)
        ))

    def test_strip(self):
        self.assertEqual(strip(tuple()), tuple())
        self.assertEqual(strip(((0, 0, 0),)), tuple())
        source = (
            (0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 1, 0, 0, 0),
            (0, 0, 1, 0, 1, 1, 0),
            (0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 1, 1, 0, 0),
            (0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0)
        )
        self.assertEqual(left_margin(source), 2)
        self.assertEqual(right_margin(source), 1)
        self.assertEqual(strip(source),
            (
                (0, 1, 0, 0),
                (1, 0, 1, 1),
                (0, 0, 0, 0),
                (0, 1, 1, 0),
                (0, 1, 0, 0)
            )
        )

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


    def test_sequence(self):
        m =  (
              (0, 1, 0, 0, 0, 0, 0),
              (0, 0, 1, 0, 0, 0, 0),
              (1, 1, 1, 0, 0, 0, 0),
              (0, 0, 0, 0, 0, 1, 1),
              (0, 0, 0, 0, 0, 1, 1),
              (0, 0, 0, 0, 0, 0, 0),
              (1, 1, 1, 0, 0, 0, 0)
            )
        self.assertEqual(next_state(m),
            (
              (1, 0, 1, 0, 0, 0, 0),
              (0, 1, 1, 0, 0, 0, 0),
              (0, 1, 0, 0, 0, 1, 1),
              (0, 0, 0, 0, 0, 1, 1),
              (0, 1, 0, 0, 0, 0, 0),
              (0, 1, 0, 0, 0, 0, 0),
              (0, 1, 0, 0, 0, 0, 0)
            ))
        self.assertEqual(next_state(next_state(m)),
            (
              (0, 0, 1, 0, 0, 0, 0),
              (1, 0, 1, 0, 0, 0, 0),
              (0, 1, 1, 0, 0, 1, 1),
              (0, 0, 0, 0, 0, 1, 1),
              (0, 0, 0, 0, 0, 0, 0),
              (1, 1, 1, 0, 0, 0, 0),
            ))

    def test_life_counter_0(self):
        self.assertEqual(life_counter(
            (
              (0, 1, 0, 0, 0, 0, 0),
              (0, 0, 1, 0, 0, 0, 0),
              (1, 1, 1, 0, 0, 0, 0),
              (0, 0, 0, 0, 0, 1, 1),
              (0, 0, 0, 0, 0, 1, 1),
              (0, 0, 0, 0, 0, 0, 0),
              (1, 1, 1, 0, 0, 0, 0)
            ), 0), 12)


    def test_Given(self):
        self.assertEqual(life_counter(
            (
              (0, 1, 0, 0, 0, 0, 0),
              (0, 0, 1, 0, 0, 0, 0),
              (1, 1, 1, 0, 0, 0, 0),
              (0, 0, 0, 0, 0, 1, 1),
              (0, 0, 0, 0, 0, 1, 1),
              (0, 0, 0, 0, 0, 0, 0),
              (1, 1, 1, 0, 0, 0, 0)
            ), 4), 15)
