from text_holes_golf import *
from unittest.case import TestCase

class golfTest(TestCase):

    def testGiven(self):
        self.assertEqual(1, golf(["xxx","x x", "xxx"]))

        self.assertEqual(1, golf([
            "Lorem Ipsum?",
            "Of course!!!",
            "Fine! good buy!"]))


        self.assertEqual(2, golf([
            "xxxxx",
            "x x x",
            "xxxxx"]))

        self.assertEqual(3, golf([
            "How are you doing?",
            "I'm fine. OK.",
            "Lorem Ipsum?",
            "Of course!!!",
            "1234567890",
            "0        0",
            "1234567890",
            "Fine! good buy!"]))
