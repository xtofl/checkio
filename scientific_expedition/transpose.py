
def transpose(rows):
    if not rows: return []
    return [[row[i] for row in rows] for i in range(len(rows[0]))]

from unittest import TestCase


class TestTranspose(TestCase):
    def test_One(self):
        self.assertEqual(transpose([]), [])
        self.assertEqual(transpose([[1]]), [[1]])
        self.assertEqual(transpose([[1, 2]]), [[1], [2]])