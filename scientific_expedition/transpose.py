from unittest import TestCase

def transpose(matrix):
    return matrix

class TestTranspose(TestCase):
    def test_One(self):
        self.assertEqual(transpose([]), [])