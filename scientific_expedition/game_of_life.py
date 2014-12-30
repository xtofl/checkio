from itertools import dropwhile, takewhile


def life_counter(state, ticks):
    for t in range(ticks):
        state = next_state(state)
    return sum(sum(r) for r in state)
        

def next_state(state):
    enlarged = grow(state)
    processed = apply_live_rule(enlarged, count_live_neighbors(enlarged))
    return shrink(processed)


def count_live_neighbors(state):
    return tuple(tuple(count_live_neighbors_row(state, r))
                 for r in range(len(state)))


def apply_live_rule(state, count_matrix):
    return tuple(
        tuple(int(next_cell_state(current, cnt))
              for current, cnt in zip(rstate, rcount))
        for (rstate, rcount) in zip(state, count_matrix))


def next_cell_state(current, live_neighbors):
    if current:
        return 1 < live_neighbors < 4
    else:
        return live_neighbors == 3

neighbors = ((-1, -1), (-1, 0), (-1, 1),
             ( 0, -1),          ( 0, 1),
             ( 1, -1), ( 1, 0), ( 1, 1))


def count_alive_around(state, row, col):
    count = 0
    for r, c in ((row + dr, col + dc) for dr, dc in neighbors):
        if 0 <= r < len(state) and 0 <= c < len(state[0]):
            count += state[r][c]
    return count


def count_live_neighbors_row(state, r):
    yield from (count_alive_around(state, r, c) for c in range(len(state[r])))


def grow(state):
    if not state:
        return tuple()
    zeroes = (0, ) * (2 + len(state[0]))
    return \
        (zeroes, ) + \
        tuple(
            (0, ) + row + (0, ) for row in state
        ) + \
        (zeroes, )


def shrink(state):
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


def left_margin(state):
    return min(sum(1 for _ in takewhile(lambda c: not c, row))
               for row in state)


def right_margin(state):
    return min(sum(1 for _ in takewhile(lambda c: not c, reversed(row)))
               for row in state)


from unittest import TestCase


class TestGOL(TestCase):

    def test_count_live_cells(self):
        m = (
            (0, 0, 0, 0, 0),
            (0, 0, 0, 1, 0),
            (0, 0, 1, 1, 0),
            (0, 0, 0, 0, 0)
        )
        self.assertEqual(count_alive_around(m, 0, 0), 0)
        self.assertEqual(count_alive_around(m, 0, 2), 1)

    def test_nbmatrix(self):
        m = (
            (0, 0, 0, 0, 0),
            (0, 0, 0, 1, 0),
            (0, 0, 1, 1, 0),
            (0, 0, 0, 0, 1)
        )
        self.assertEqual(count_live_neighbors(m), (
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
        self.assertEqual(apply_live_rule(m, c), (
            (0, 0, 0, 0, 0),
            (0, 0, 1, 1, 0),
            (0, 0, 1, 1, 1),
            (0, 0, 0, 1, 0)
        ))

    def test_enlarge(self):
        self.assertEqual(grow(((0,),)), ((0, 0, 0), (0, 0, 0), (0, 0, 0)))
        self.assertEqual(grow(tuple()), tuple())

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
        self.assertEqual(shrink(tuple()), tuple())
        self.assertEqual(shrink(((0, 0, 0),)), tuple())
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
        self.assertEqual(shrink(source),
            (
                (0, 1, 0, 0),
                (1, 0, 1, 1),
                (0, 0, 0, 0),
                (0, 1, 1, 0),
                (0, 1, 0, 0)
            )
        )

    def test_liveCell(self):
        self.assertFalse(next_cell_state(1, 0))
        self.assertFalse(next_cell_state(1, 1))
        self.assertTrue(next_cell_state(1, 2))
        self.assertTrue(next_cell_state(1, 3))
        self.assertFalse(next_cell_state(1, 4))
        self.assertFalse(next_cell_state(1, 8))

    def test_deadCell(self):
        self.assertFalse(next_cell_state(0, 0))
        self.assertFalse(next_cell_state(0, 1))
        self.assertFalse(next_cell_state(0, 2))
        self.assertTrue(next_cell_state(0, 3))
        self.assertFalse(next_cell_state(0, 4))
        self.assertFalse(next_cell_state(0, 8))


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

        self.assertEqual(life_counter(
            (
                (0,1,0),
                (0,0,1),
                (1,1,1),
            ), 50), 5)

        self.assertEqual(life_counter(
            (
                (0,1,0),
                (0,0,1),
                (1,1,1),
            ), 100), 5)


    def test_from_github(self):
        """
        TESTS is a dict with all you tests.
        Keys for this will be categories' names.
        Each test is dict with
            "input" -- input data for user function
            "answer" -- your right answer
            "explanation" -- not necessary key, it's using for additional info in animation.
        """

        TESTS = {
            "Basics": [
                {
                    "input": [((0, 1, 0, 0, 0, 0, 0), (0, 0, 1, 0, 0, 0, 0), (1, 1, 1, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 1, 1), (0, 0, 0, 0, 0, 1, 1), (0, 0, 0, 0, 0, 0, 0),
                               (1, 1, 1, 0, 0, 0, 0)), 4],
                    "answer": 15,
                    "explanation": (0, 7, 0, 6),
                },
                {
                    "input": [((0, 1, 0, 0, 0, 0, 0), (0, 0, 1, 0, 0, 0, 0), (1, 1, 1, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 1, 1), (0, 0, 0, 0, 0, 1, 1), (0, 0, 0, 0, 0, 0, 0),
                               (1, 1, 1, 0, 0, 0, 0)), 15],
                    "answer": 14,
                    "explanation": (0, 7, -3, 6),
                },
                {
                    "input": [((0, 1, 0), (0, 0, 1), (1, 1, 1)), 50],
                    "answer": 5,
                    "explanation": (0, 15, 0, 14),
                },
                {
                    "input": [((1, 1, 0, 1, 1), (1, 1, 0, 1, 1), (0, 0, 0, 0, 0), (1, 1, 0, 1, 1),
                               (1, 1, 0, 1, 1)), 100],
                    "answer": 16,
                    "explanation": (0, 4, 0, 4),
                }
            ],
            "Extra": [
                {
                    "input": [
                        ((0, 0, 0, 0, 0, 0, 1, 0), (1, 1, 0, 0, 0, 0, 0, 0), (0, 1, 0, 0, 0, 1, 1, 1)),
                        129],
                    "answer": 2,
                    "explanation": (-4, 18, -6, 11),
                },
                {
                    "input": [((0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1),
                               (1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1),
                               (1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1),
                               (0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0),
                               (1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1),
                               (1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1),
                               (1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0)), 100],
                    "answer": 56,
                    "explanation": (-1, 13, -1, 13),
                },
                {
                    "input": [((0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
                               (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
                               (1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1),
                               (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
                               (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
                               (0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0),
                               (0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0),
                               (0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0)), 42],
                    "answer": 36,
                    "explanation": (-12, 10, -1, 16),
                },
                {
                    "input": [((0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1), (0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1),
                               (1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1),
                               (0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1), (0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1),
                               (0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1), (0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1)), 100],
                    "answer": 33,
                    "explanation": (-9, 15, -5, 22),
                },

                {
                    "input": [((0, 1, 0), (0, 0, 1), (1, 1, 1)), 999],
                    "answer": 5,
                    "explanation": None,
                },
                {
                    "input": [
                        ((0, 1, 0, 0, 0, 0, 1, 0), (1, 0, 0, 0, 0, 0, 0, 1), (1, 1, 1, 0, 0, 1, 1, 1)),
                        999],
                    "answer": 10,
                    "explanation": None,
                },
                {
                    "input": [((0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1), (0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1),
                               (0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1), (0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0),
                               (1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1), (0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1),
                               (0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1), (0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1)), 100],
                    "answer": 52,
                    "explanation": (-18, 20, -5, 20),
                },
                {
                    "input": [((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0),
                               (0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0),
                               (0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)), 10],
                    "answer": 22,
                    "explanation": (0, 17, 0, 16),
                },
                {
                    "input": [((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0),
                               (0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                               (0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0),
                               (0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0),
                               (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)), 20],
                    "answer": 0,
                    "explanation": (0, 17, 0, 16),
                },
                {
                    "input": [((0, 0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 0, 0, 1, 1, 1), (0, 0, 0, 0, 0, 1, 0, 0),
                               (0, 0, 0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 0, 0, 0, 0), (1, 1, 1, 0, 0, 0, 0, 0),
                               (0, 0, 0, 0, 0, 1, 1, 1), (0, 0, 0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 0, 0, 1, 0),
                               (1, 1, 1, 0, 0, 0, 0, 0)), 100],
                    "answer": 3,
                    "explanation": (-1, 10, -2, 7),
                },
                {
                    "input": [[[0, 1, 1, 1, 1, 1, 1, 1, 0, 0], [0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
                               [0, 0, 1, 0, 0, 0, 0, 0, 1, 1], [1, 0, 0, 1, 0, 0, 1, 1, 1, 1],
                               [1, 0, 1, 0, 0, 1, 0, 1, 1, 0], [0, 1, 1, 0, 0, 1, 0, 1, 1, 1],
                               [1, 0, 1, 0, 1, 1, 1, 0, 1, 1], [0, 1, 1, 1, 0, 0, 1, 1, 1, 1],
                               [0, 0, 1, 0, 1, 1, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 1, 1, 1, 1]], 50],
                    "answer": 74,
                    "explanation": (-6, 13, -5, 24),
                },
                {
                    "input": [[[1, 1, 1, 1, 0, 1, 1, 0, 1, 1], [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                               [0, 1, 0, 1, 1, 0, 1, 1, 1, 1], [0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
                               [0, 1, 1, 1, 0, 1, 1, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0, 1, 1, 0],
                               [1, 0, 1, 0, 0, 0, 0, 0, 1, 1], [1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                               [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 1, 1, 0, 1, 0, 1, 1]], 50],
                    "answer": 79,
                    "explanation": (-5, 17, -14, 16),
                },
                {
                    "input": [[[0, 0, 1, 1, 1, 1, 0, 1, 0, 0], [1, 1, 0, 0, 1, 0, 1, 1, 1, 0],
                               [0, 1, 1, 1, 1, 1, 0, 0, 1, 0], [0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
                               [1, 1, 0, 1, 0, 0, 0, 0, 1, 0], [1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                               [1, 0, 0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                               [1, 0, 0, 1, 0, 0, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 1, 0, 1, 0]], 50],
                    "answer": 81,
                    "explanation": (-9, 15, -4, 24),
                },
                {
                    "input": [[[1, 0, 0, 0, 1, 0, 0, 0, 1, 0], [1, 1, 0, 0, 1, 0, 1, 0, 1, 0],
                               [1, 0, 0, 0, 0, 1, 1, 1, 1, 1], [0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 1, 1, 1, 1, 0, 1, 1, 0], [0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
                               [0, 1, 0, 0, 1, 0, 0, 0, 0, 0], [1, 1, 0, 1, 0, 0, 0, 0, 1, 1],
                               [0, 1, 1, 1, 1, 1, 0, 0, 0, 1], [1, 1, 0, 0, 0, 1, 1, 1, 1, 0]], 50],
                    "answer": 18,
                    "explanation": (-3, 16, -5, 13),
                }


            ]
        }
        for name, cases in TESTS.items():
            for case in cases:
                state = case["input"][0]
                ticks = case["input"][1]
                answer = case["answer"]
                self.assertEqual(life_counter(state, ticks), answer)
