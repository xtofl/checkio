
def transpose(rows):
    return tuple(zip(*rows))

from unittest import TestCase


class TestTranspose(TestCase):
    def test_One(self):
        self.assertEqual(transpose([]), tuple())
        self.assertEqual(transpose([[1]]), ((1,),))
        self.assertEqual(transpose([[1, 2]]), ((1,), (2,)))