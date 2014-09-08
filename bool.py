
def boolean(val1, val2, op):
    return {
        "conjunction": lambda a, b: a and b,
        "disjunction": lambda a, b: a or b,
        "implication": lambda a, b: not a or b,
        "exclusive": lambda a, b: (a or b) and not (a and b),
        "equivalence": lambda a, b: a == b
    }[op](val1, val2)


from unittest import TestCase


class TestBool(TestCase):
    def test_One(self):
        self.assertEqual(True, boolean(True, True, "conjunction"))
        self.assertEqual(False, boolean(False, True, "conjunction"))
