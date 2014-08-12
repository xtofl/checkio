from functools import partial
from itertools import combinations


def make_ordering(words, a, b):
    occurences = filter(lambda w: a in w and b in w, words)
    if occurences:
        return occurences[0]


def make_cmp(words):

    def f(a, b):
        ordering = make_ordering(words, a, b)
        if ordering:
            ia = ordering.find(a)
            ib = ordering.find(b)
            return cmp(ia, ib)
        else:
            return cmp(a, b)

    return f


def can_be_sorted(lowercase_words, characters):
    return True
    can_be_combined = lambda xy: make_ordering(lowercase_words, *xy)
    completely_ordered = all(map(can_be_combined, combinations(characters, 2)))
    return completely_ordered


def checkio(data):
    lowercase_words = [x.lower() for x in data]
    characters = frozenset("".join(data))
    comparator = make_cmp(lowercase_words)

    if can_be_sorted(lowercase_words, characters):
        return "".join(sorted(characters, cmp=comparator))
    else:
        return "".join(lowercase_words)

from unittest import TestCase

class TestTheOrder(TestCase):
    def testJustConcat(self):
        self.assertEqual("zwacbd", checkio(["acb", "bd", "zwa"]))

    def testPasteIn(self):
        self.assertEqual("kadlsm", checkio(["klm", "kadl", "lsm"]))

    def testLatinOrder(self):
        self.assertEqual("abc", checkio(["a", "b", "c"]))

    def testEachSymbolOnlyOnce(self):
        self.assertEqual("azs", checkio(["aazzss"]))

    def testConcatenateAndPasteIn(self):
        self.assertEqual("dfrtyg", checkio(["dfg", "frt", "tyg"]))

"""
The Robots have found an encrypted message. We cannot decrypt it at the moment, but we can take the first steps towards
 doing so. You have a set of "words", all in lower case, and each word contains symbols in "alphabetical order".
 (it's not your typical alphabetical order, but a new and different order.)

 We need to determine the order of the symbols from each "word" and create a single "word" with all of these symbols,
 placing them in the new alphabetial order.

 In some cases, if we cannot determine the order for several symbols, you should use the traditional latin
 alphabetical order. For example: Given words "acb", "bd", "zwa". As we can see "z" and "w" must be before "a" and
 "d" after "b". So the result is "zwacbd".

Input: Words as a list of strings.
Output: The order as a string.
Precondition: For each test, there can be the only one solution.
0 < |words| < 10"""