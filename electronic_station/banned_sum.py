__author__ = 'xtofl'

def checkio(terms, s=0):
    if not terms:
        return s
    return checkio(terms[1:], s+terms[0])


from unittest import TestCase


class Test(TestCase):
    def test_One(self):
        def eq(s, terms):
            self.assertEqual(s, checkio(terms))

        eq(0, [])
        eq(1, [1])
        eq(2, [1, 1])