from unittest import TestCase


def checkio(expr):
    closing_brackets = {
        '(': ')',
        '[': ']',
        '{': '}'
    }
    expect_closing = []
    for c in expr:
        if c in closing_brackets.keys():
            expect_closing.append(closing_brackets[c])
        elif c in closing_brackets.values():
            if c == expect_closing[-1]:
                expect_closing.pop()
            else:
                return False
    return not expect_closing

class TestBrackets(TestCase):
    def test_One(self):
        def valid(expr):
            self.assertTrue(checkio(expr), expr)
        def invalid(expr):
            self.assertFalse(checkio(expr), expr)
        valid("")
        valid("()")
        invalid("(")
        valid("((5+3)*2+1)") == True
        valid("{[(3+1)+2]+}") == True
        invalid("(3+{1-1)}") == False
        valid("[1+1]+(2*2)-{3/3}") == True
        invalid("(({[(((1)-2)+3)-3]/3}-3)") == False
        valid("2+3") == True
