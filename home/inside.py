
def inside(polygon, point):
    return True


from unittest import TestCase


class TestInside(TestCase):
    def test_One(self):
        polygon = ((0, 0), (0, 1), (1, 1), (1, 0))
        self.assertTrue(inside(polygon, (0.5, 0.5)))