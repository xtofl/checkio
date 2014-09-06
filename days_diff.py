from unittest import TestCase

from datetime import datetime

def days_diff(date1, date2):
    return abs((datetime(*date1) - datetime(*date2)).days)

class Test(TestCase):
    def test_One(self):
        self.assertEqual(3, days_diff((1982, 4, 19), (1982, 4, 22)))
        self.assertEqual(238, days_diff((2014, 1, 1), (2014, 8, 27)))
        self.assertEqual(238, days_diff((2014, 8, 27), (2014, 1, 1)))