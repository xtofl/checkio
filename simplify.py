__mission__ = """http://www.checkio.org/mission/simplification/share/cd052a5416a6e8b459e74b63451b9c30/"""

from unittest import TestCase


class Expr:
    def fmt(self):
        return "?"

class Constant(Expr):
    def __init__(self, value):
        self.value = value

    def negative(self):
        return self.value < 0

    def fmt(self):
        return str(self.value)


class Power(Expr):
    def __init__(self, exponent):
        self.exponent = exponent

    def fmt(self):
        return "x**{}".format(self.exponent)


class Sum(Expr):
    def __init__(self, terms):
        self.terms = terms

    def __str__(self):
        return self.terms[0].fmt() + \
               "".join([
                   ('-' if t.negative() else '+') + t.fmt()
                   for t in self.terms[1:]])


def parse(expr):
    """returns an expression tree"""
    return Sum([Power(2), Constant(-1)])


def simplify(expr):
    return str(parse(expr))


class TestSimplify(TestCase):

    def test_Format(self):
        self.assertEqual("1+2", str(Sum([Constant(1), Constant(2)])))

    def test_Given(self):
        self.assertEqual("x**2-1", simplify("(x-1)*(x+1)"))
        self.assertEqual("x**2+2*x+1", simplify("(x+1)*(x+1)"))
        self.assertEqual("x**2+6*x", simplify("(x+3)*x*2-x*x"))
        self.assertEqual("x**3+x**2+x", simplify("x+x*x+x*x*x"))
        self.assertEqual("x**4+3*x+6", simplify("(2*x+3)*2-x+x*x*x*x"))
        self.assertEqual("0", simplify("x*x-(x-1)*(x+1)-1"))
        self.assertEqual( "-x", simplify("5-5-x"))
        self.assertEqual("-1", simplify("x*x*x-x*x*x-1"))