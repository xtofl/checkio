class Building(object):
    def __init__(self, south, west, width_WE, width_NS, height=10):
        self.area = lambda: width_WE * width_NS
        self.volume = lambda: width_WE * width_NS * height
        self.corners = lambda:\
            {
                "north-west": [south + width_NS, west],
                "north-east": [south + width_NS, west + width_WE],
                "south-west": [south, west],
                "south-east": [south, west + width_WE]
            }

        #the only one I couldn't do with a lambda :(
        self.repr = "Building({}, {}, {}, {}, {})".format(\
            south, west, width_WE, width_NS, height
            )

    def __repr__(self):
        return self.repr



from unittest import TestCase

class TestBuilding(TestCase):
    def test_One(self):
        self.assertEqual(5.25, Building(1, 2.5, 4.2, 1.25).area())
        self.assertEqual(530.25, Building(1, 2.5, 4.2, 1.25, 101).volume())
        self.assertEqual({'north-west': [3, 2], "north-east": [3, 4], "south-west": [1, 2], "south-east": [1, 4]}, Building(1, 2, 2, 2).corners())
        self.assertEqual("Building(0, 0, 10.5, 2.546, 10)", str(Building(0, 0, 10.5, 2.546)))