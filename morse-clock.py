
def encode_digit(digit, places):
    return {"0": "....",
            "1": "...-",
            "2": "..-.",
            "3": "..--",
            "4": ".-..",
            "5": ".-.-",
            "6": ".--.",
            "7": ".---",
            "8": "-...",
            "9": "-..-"
    }[digit][4-places:]

def expand(part):
    if len(part) < 2: return "0"+part
    else: return part

def checkio(timestring):
    parts = map(expand, timestring.split(":"))
    digits = "".join(parts)
    encoded_digits = map(lambda x: encode_digit(*x), zip(digits, [2, 4, 3, 4, 3, 4]))
    i = iter(encoded_digits)
    per_two = zip(i, iter(i))
    return " : ".join(map(lambda part: "{} {}".format(*part), per_two))


from unittest import TestCase

class TestMorseClock(TestCase):

    def testDigit(self):
        self.assertEqual("....", encode_digit("0", 4))
        self.assertEqual("...-", encode_digit("1", 4))

    def testGiven(self):
        self.assertEqual(".- .... : .-- .--- : -.. -..-", checkio("10:37:49"))
        self.assertEqual("-. ...- : .-- .-.. : -.- .--.", checkio("21:34:56"))
        self.assertEqual(".. .... : ... ...- : ... ..-.", checkio("00:1:02" ))
        self.assertEqual("-. ..-- : -.- -..- : -.- -..-", checkio("23:59:59"))