import re
def boolean(x, y, op):
    definition="""
     x | y | conjunction | disjunction | implication | exclusive | equivalence |
    --------------------------------------
     0 | 0 |  0  |  0  |  1  |  0  |  1  |
     1 | 0 |  0  |  1  |  0  |  1  |  0  |
     0 | 1 |  0  |  1  |  1  |  1  |  0  |
     1 | 1 |  1  |  1  |  1  |  0  |  1  |
    --------------------------------------
    """.splitlines()
    operators = [x_.strip() for x_ in re.split("\|", definition[1])[2:] if x_]

    table = {op: {} for op in operators}
    for entry in definition[3:-2]:
        values = [int(v.strip()) for v in re.split("\|", entry) if v]
        a, b = values[0:2]
        for operator, value in zip(operators, values[2:]):
            table[operator][(a, b)] = value

    return table[op][(x, y)]

from unittest import TestCase


class TestBool(TestCase):
    def test_One(self):
        self.assertEqual(1, boolean(1, 1, "conjunction"))
        self.assertEqual(0, boolean(0, 1, "conjunction"))
