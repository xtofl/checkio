from itertools import product, chain
from operator import mul, add
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
        return self


class Power(Expr):
    def __init__(self, exponent):
        self.exponent = exponent

    def abs_fmt(self):
        return "x**{}".format(self.exponent)

    def negative(self):
        return False

    def simplify(self):
        return self

    def __eq__(self, other):
        if not type(other) is Power:
            return False
        return self.exponent == other.exponent


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

    def __repr__(self):
        return "Sum({})".format(tuple(repr(t) for t in self.terms))

    def __eq__(self, other):
        if self is other:
            return True
        if not type(other) is Sum:
            return False
        return self.terms == other.terms


class Product(Expr):
    def __init__(self, *factors):
        self.factors = tuple(factors)

    def negative(self):
        return sum((f.negative() for f in self.factors)) % 2 == 1

    def power_factors(self):
        powers = tuple(f for f in self.factors if type(f) is Power)
        exponent = reduce(add, (p.exponent for p in powers), 0)
        return Power(exponent)

    def constant_factor(self):
        constants = (f for f in self.factors if type(f) is Constant)
        constant = Constant(reduce(mul, (c.value for c in constants), 1)) if constants else None
        return constant

    def sum_factors(self):
        return (f for f in self.factors if type(f) is Sum)

    def simplify(self):
        constant = self.constant_factor()

        simple_factors = (f for f in (constant, self.power_factors()) if f)

        sums = self.sum_factors()
        if not sums:
            return Product(simple_factors)
        else:
            return Sum(*(Product(*chain(simple_factors, c)) for c in product(sums)))

    def abs_fmt(self):
        return "*".join((f.abs_fmt() for f in self.factors))

    def __repr__(self):
        return "Product({})".format(tuple(repr(f) for f in self.factors))

    def __eq__(self, other):
        if other is self:
            return True
        if not type(other) is Product:
            return False
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

        self.assertEqual(1, len(Product(Power(1)).factors))
        self.assertSequenceEqual((Power(1),), Product(Power(1)).factors)

    def test_Product_PowerTerm(self):
        self.assertEqual(Power(0), Product(Constant(5)).power_factors())
        self.assertEqual(Power(2), Product(Power(2)).power_factors())

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