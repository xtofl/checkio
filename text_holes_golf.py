from unittest.case import TestCase
import re

def matches(line):
    return re.finditer(r"\S\s\S", line)

def golf(text):
    def iterate(text):
        for i, line in enumerate(text[1:-1]):
            for s in matches(line):
                isalpha = lambda n: re.match(r"\S{3}", text[n][s.start():s.end()])
                neighbors = map(isalpha, [i, i+2])
                if all(neighbors):
                    yield i, s
    return len(list(iterate(text)))


class golfTest(TestCase):

    def testMatches(self):
        self.assertEqual(["c d"], map(lambda m: m.string[m.start():m.end()], matches("abc def")))
        self.assertEqual(["c d"], map(lambda m: m.string[m.start():m.end()], matches("a  bc def")))

    def testGiven(self):
        self.assertEqual(1, golf([
            "Lorem Ipsum?",
            "Of course!!!",
            "Fine! good buy!"]))

        self.assertEqual(3, golf([
            "How are you doing?",
            "I'm fine. OK.",
            "Lorem Ipsum?",
            "Of course!!!",
            "1234567890",
            "0        0",
            "1234567890",
            "Fine! good buy!"]))
