
def inside(polygon, point):
    return True

def intersects(segment, y):
    ((x0, y0), (x1, y1)) = segment
    if y0 == y1:
        return y == y1
    return y0 <= y < y1 or y1 <= y < y0

from unittest import TestCase


class TestInside(TestCase):

    def test_intersect(self):
        self.assertTrue(intersects(((0, 0), (1, 0)), y=0))
        self.assertTrue(intersects(((0, 0), (0, 1)), y=.5))
        self.assertFalse(intersects(((0, 0), (0, 1)), y=-1))
        self.assertFalse(intersects(((0, 0), (0, 1)), y=2))

    def test_intersect_with_edge_yields_false_if_segment_below(self):
        self.assertFalse(intersects(((0, 0), (1, 1)), y=1))

    def test_intersect_with_edge_yields_true_if_segment_above(self):
        self.assertTrue(intersects(((0, 0), (1, 1)), y=0))

    def test_One(self):
        polygon = ((0, 0), (0, 1), (1, 1), (1, 0))
        self.assertTrue(inside(polygon, (0.5, 0.5)))
        self.assertFalse(inside(polygon, (10, .5)))