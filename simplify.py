from itertools import product, chain
from operator import mul
from functools import reduce
from unittest import TestCase

__mission__ = """http://www.checkio.org/mission/simplification/share/cd052a5416a6e8b459e74b63451b9c30/"""


class Expr:
    def __repr__(self):
        return self.abs_fmt()


class Constant(Expr):
    def __init__(self, value):
        self.value = value

    def negative(self):
        return self.value < 0

    def abs_fmt(self):
        return str(abs(self.value))

    def simplify(self):
        return [self]


class Power(Expr):
    def __init__(self, exponent):
        self.exponent = exponent

    def abs_fmt(self):
        return "x**{}".format(self.exponent)

    def negative(self):
        return False

    def simplify(self):
        return self


class Sum(Expr):
    def __init__(self, *terms):
        self.terms = tuple(terms)

    def fmt(self):
        return self.terms[0].abs_fmt() + \
               "".join([
                   ('-' if t.negative() else '+') + t.abs_fmt()
                   for t in self.terms[1:]])

    def simplify(self):
        return reduce(lambda lst, t: lst+(t,), (t.simplify() for t in self.terms))

    def abs_fmt(self):
        return "+".join((f.abs_fmt() for f in self.terms))

    def __eq__(self, other):
        return self.terms == other.terms


class Product(Expr):
    def __init__(self, *factors):
        self.factors = tuple(factors)

    def negative(self):
        return sum((f.negative() for f in self.factors)) % 2 == 1

    def simplify(self):
        constants = (f for f in self.factors if f is Constant)
        powers = (f for f in self.factors if f is Power)
        sums = (f for f in self.factors if f is Sum)

        constant = Constant(reduce(mul, constants, 1)) if constants else None
        power = Power(reduce(sum, (p.exponent for p in powers), 0)) if powers else None
        simple_factors = tuple(f for f in (constant, power) if f)

        if not sums:
            return Product(simple_factors)
        else:
            return Sum((Product(chain(simple_factors, c)) for c in product(sums)))

    def abs_fmt(self):
        return "*".join((f.abs_fmt() for f in self.factors))

    def __eq__(self, other):
        return self.factors == other.factors


def parse(expr):
    """returns an expression tree"""
    return Sum(Power(2), Constant(-1))


def simplify(expr):
    return str(parse(expr))


class Reductions:

    @staticmethod
    def distribute(factor, terms):
        return tuple((t, factor) for t in terms)

class TestSimplify(TestCase):

    def test_Product(self):
        self.assertEqual(True, Product(Constant(-1), Constant(1)).negative())

    def test_Format(self):
        self.assertEqual("1+2", Sum(Constant(1), Constant(2)).fmt())

        self.assertEqual("8*x**5", Product(Constant(-8), Power(5)).abs_fmt())
        self.assertEqual("8*x**5", Product(Constant(8), Power(5)).abs_fmt())

        term1 = Product(Constant(8), Power(5))
        term2 = Product(Constant(-2), Power(2))
        self.assertEqual("8*x**5-2*x**2", Sum(term1, term2).fmt())
        self.assertEqual(term1, term1)


    def test_Simplification(self):
        term1 = Product(Constant(8), Power(5))
        term2 = Product(Constant(-2), Power(2))
        s = Sum(term1, term2)
        factor = Constant(5)
        product = Product(Constant(5), s) # 5 * (8x^5 - 2x^2) = 40x^5 -10x^2
        simplified = product.simplify()
        self.assertTrue(simplified is Sum)
        self.assertEqual(Sum(Product(Constant(40), Power(5)), Product(Constant(-10), Power(2))),
                         simplified)

    def _test_Given(self):
        self.assertEqual("x**2-1", simplify("(x-1)*(x+1)"))
        self.assertEqual("x**2+2*x+1", simplify("(x+1)*(x+1)"))
        self.assertEqual("x**2+6*x", simplify("(x+3)*x*2-x*x"))
        self.assertEqual("x**3+x**2+x", simplify("x+x*x+x*x*x"))
        self.assertEqual("x**4+3*x+6", simplify("(2*x+3)*2-x+x*x*x*x"))
        self.assertEqual("0", simplify("x*x-(x-1)*(x+1)-1"))
        self.assertEqual( "-x", simplify("5-5-x"))
        self.assertEqual("-1", simplify("x*x*x-x*x*x-1"))