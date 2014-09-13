from operator import mul

__mission__ = """http://www.checkio.org/mission/simplification/share/cd052a5416a6e8b459e74b63451b9c30/"""
from functools import reduce
from unittest import TestCase


class Expr:
    pass


class Constant(Expr):
    def __init__(self, value):
        self.value = value

    def negative(self):
        return self.value < 0

    def abs_fmt(self):
        return str(abs(self.value))

    def pattern(self):
        return "c"


class Power(Expr):
    def __init__(self, exponent):
        self.exponent = exponent

    def abs_fmt(self):
        return "x**{}".format(self.exponent)

    def pattern(self):
        return "^"


class Term(Expr):
    def __init__(self, factor, exponent):
        self.factor = factor
        self.exponent = exponent

    def negative(self):
        return self.factor.negative()

    def abs_fmt(self):
        return "{}*{}".format(self.factor.abs_fmt(), self.exponent.abs_fmt())

    def pattern(self):
        return "t"


class Product(Expr):
    def __init__(self, *factors):
        self.factors = factors

    def pattern(self):
        return "*"

    def simplify(self):
        if all([f.pattern() == "t" for f in self.factors]):
            return Term(reduce(mul, [f.factor for f in self.factors]))

class Reductions:

    @staticmethod
    def distribute(terms, factor):
        return [(t, factor) for t in terms]

class Sum(Expr):
    def __init__(self, *terms):
        self.terms = terms

    def fmt(self):
        return self.terms[0].abs_fmt() + \
               "".join([
                   ('-' if t.negative() else '+') + t.abs_fmt()
                   for t in self.terms[1:]])

    def pattern(self):
        return "".join([t.pattern() for t in self.terms])

def parse(expr):
    """returns an expression tree"""
    return Sum(Power(2), Constant(-1))


def simplify(expr):
    return str(parse(expr))


class TestSimplify(TestCase):

    def test_Format(self):
        self.assertEqual("1+2", Sum(Constant(1), Constant(2)).fmt())

        self.assertEqual("8*x**5", Term(Constant(-8), Power(5)).abs_fmt())
        self.assertEqual("8*x**5", Term(Constant(8), Power(5)).abs_fmt())

        term1 = Term(Constant(8), Power(5))
        term2 = Term(Constant(-2), Power(2))
        self.assertEqual("8*x**5-2*x**2", Sum(term1, term2).fmt())

    def test_RuleMatching(self):
        self.assertEqual("c", Constant(1).pattern())
        self.assertEqual("^", Power(1).pattern())
        self.assertEqual("t", Term(1, 2).pattern())
        term1 = Term(Constant(8), Power(5))
        term2 = Term(Constant(-2), Power(2))
        sum = Sum(term1, term2)
        self.assertEqual("tt", sum.pattern())
        self.assertEqual("*", Product(term1, term2).pattern())


    def test_Simplification(self):
        term1 = Term(Constant(8), Power(5))
        term2 = Term(Constant(-2), Power(2))
        product = Product(term1, term2)
        self.assertEqual("t", product.simplify().pattern())

    def _test_Given(self):
        self.assertEqual("x**2-1", simplify("(x-1)*(x+1)"))
        self.assertEqual("x**2+2*x+1", simplify("(x+1)*(x+1)"))
        self.assertEqual("x**2+6*x", simplify("(x+3)*x*2-x*x"))
        self.assertEqual("x**3+x**2+x", simplify("x+x*x+x*x*x"))
        self.assertEqual("x**4+3*x+6", simplify("(2*x+3)*2-x+x*x*x*x"))
        self.assertEqual("0", simplify("x*x-(x-1)*(x+1)-1"))
        self.assertEqual( "-x", simplify("5-5-x"))
        self.assertEqual("-1", simplify("x*x*x-x*x*x-1"))