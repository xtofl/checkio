import text_holes_golf
from unittest.case import TestCase

class golfTest(TestCase):

    def testGiven(self):
        self.assertEqual(1, text_holes_golf.golf(["xxx","x x", "xxx"]))

        self.assertEqual(1, text_holes_golf.golf([
            "Lorem Ipsum?",
            "Of course!!!",
            "Fine! good buy!"]))


        self.assertEqual(2, text_holes_golf.golf([
            "xxxxx",
            "x x x",
            "xxxxx"]))

        self.assertEqual(3, text_holes_golf.golf([
            "How are you doing?",
            "I'm fine. OK.",
            "Lorem Ipsum?",
            "Of course!!!",
            "1234567890",
            "0        0",
            "1234567890",
            "Fine! good buy!"]))

        self.assertEqual(5, text_holes_golf.golf([
            "J  ck wU phP  UZfhHx",
            "YNJ ugWNxKsPRasldco",
            "hnIsUlWVO EhIyoNwLNZ",
            "JEbloQ",
            "XWrjMl B CAOR hZoJ",
            "fMbJYeWgZHdbrgzcstd",
            "ycY GyuS Sblj WB",
            "fScUFqMKPOZ I",
            "ioBkDQUL",
            "QCV UweAY zm",
            " QR QOe Ew lBGRvlnK",
            "LeHduzsbakBufXD",
            " AQGRp UtLGYS",
            "nnDywuYwZTsHinW WJ",
            "jLWKFjkUYfuZL okJz",
            "HhdAZdhcKpiYkAWxg",
            "zAVNZOzyE ",
            "QRkRdf",
            "hutrJFUvrFe"]))
